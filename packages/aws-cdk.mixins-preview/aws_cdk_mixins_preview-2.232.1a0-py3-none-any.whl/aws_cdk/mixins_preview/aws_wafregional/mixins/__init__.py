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
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnByteMatchSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={"byte_match_tuples": "byteMatchTuples", "name": "name"},
)
class CfnByteMatchSetMixinProps:
    def __init__(
        self,
        *,
        byte_match_tuples: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnByteMatchSetPropsMixin.ByteMatchTupleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnByteMatchSetPropsMixin.

        :param byte_match_tuples: Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.
        :param name: A friendly name or description of the ``ByteMatchSet`` . You can't change ``Name`` after you create a ``ByteMatchSet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_byte_match_set_mixin_props = wafregional_mixins.CfnByteMatchSetMixinProps(
                byte_match_tuples=[wafregional_mixins.CfnByteMatchSetPropsMixin.ByteMatchTupleProperty(
                    field_to_match=wafregional_mixins.CfnByteMatchSetPropsMixin.FieldToMatchProperty(
                        data="data",
                        type="type"
                    ),
                    positional_constraint="positionalConstraint",
                    target_string="targetString",
                    target_string_base64="targetStringBase64",
                    text_transformation="textTransformation"
                )],
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581471ecfb00ddc6473cabd3ca04c80da0171ee64e5a6d66821c94ce32802a93)
            check_type(argname="argument byte_match_tuples", value=byte_match_tuples, expected_type=type_hints["byte_match_tuples"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if byte_match_tuples is not None:
            self._values["byte_match_tuples"] = byte_match_tuples
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def byte_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnByteMatchSetPropsMixin.ByteMatchTupleProperty"]]]]:
        '''Specifies the bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html#cfn-wafregional-bytematchset-bytematchtuples
        '''
        result = self._values.get("byte_match_tuples")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnByteMatchSetPropsMixin.ByteMatchTupleProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name or description of the ``ByteMatchSet`` .

        You can't change ``Name`` after you create a ``ByteMatchSet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html#cfn-wafregional-bytematchset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnByteMatchSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnByteMatchSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnByteMatchSetPropsMixin",
):
    '''.. epigraph::

   This is *AWS WAF Classic* documentation.

    For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
    .. epigraph::

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    The ``AWS::WAFRegional::ByteMatchSet`` resource creates an AWS WAF ``ByteMatchSet`` that identifies a part of a web request that you want to inspect.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html
    :cloudformationResource: AWS::WAFRegional::ByteMatchSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_byte_match_set_props_mixin = wafregional_mixins.CfnByteMatchSetPropsMixin(wafregional_mixins.CfnByteMatchSetMixinProps(
            byte_match_tuples=[wafregional_mixins.CfnByteMatchSetPropsMixin.ByteMatchTupleProperty(
                field_to_match=wafregional_mixins.CfnByteMatchSetPropsMixin.FieldToMatchProperty(
                    data="data",
                    type="type"
                ),
                positional_constraint="positionalConstraint",
                target_string="targetString",
                target_string_base64="targetStringBase64",
                text_transformation="textTransformation"
            )],
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnByteMatchSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::ByteMatchSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6dd74a90f738ad4966b74c29c29a94933d64f93f530b8e58d394edc1c92eb7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b054f3024c71efbc4b3e126c6e047b9cecc6fdfe5a3c2e27273d29a5954ecdea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e376061449c65d82efcf012105a21d5b9677b883a20e59e3b28ea4af842fb65)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnByteMatchSetMixinProps:
        return typing.cast(CfnByteMatchSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnByteMatchSetPropsMixin.ByteMatchTupleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "positional_constraint": "positionalConstraint",
            "target_string": "targetString",
            "target_string_base64": "targetStringBase64",
            "text_transformation": "textTransformation",
        },
    )
    class ByteMatchTupleProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnByteMatchSetPropsMixin.FieldToMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            positional_constraint: typing.Optional[builtins.str] = None,
            target_string: typing.Optional[builtins.str] = None,
            target_string_base64: typing.Optional[builtins.str] = None,
            text_transformation: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

            .. epigraph::

               This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            The bytes (typically a string that corresponds with ASCII characters) that you want AWS WAF to search for in web requests, the location in requests that you want AWS WAF to search, and other settings.

            :param field_to_match: The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.
            :param positional_constraint: Within the portion of a web request that you want to search (for example, in the query string, if any), specify where you want AWS WAF to search. Valid values include the following: *CONTAINS* The specified part of the web request must include the value of ``TargetString`` , but the location doesn't matter. *CONTAINS_WORD* The specified part of the web request must include the value of ``TargetString`` , and ``TargetString`` must contain only alphanumeric characters or underscore (A-Z, a-z, 0-9, or _). In addition, ``TargetString`` must be a word, which means one of the following: - ``TargetString`` exactly matches the value of the specified part of the web request, such as the value of a header. - ``TargetString`` is at the beginning of the specified part of the web request and is followed by a character other than an alphanumeric character or underscore (_), for example, ``BadBot;`` . - ``TargetString`` is at the end of the specified part of the web request and is preceded by a character other than an alphanumeric character or underscore (_), for example, ``;BadBot`` . - ``TargetString`` is in the middle of the specified part of the web request and is preceded and followed by characters other than alphanumeric characters or underscore (_), for example, ``-BadBot;`` . *EXACTLY* The value of the specified part of the web request must exactly match the value of ``TargetString`` . *STARTS_WITH* The value of ``TargetString`` must appear at the beginning of the specified part of the web request. *ENDS_WITH* The value of ``TargetString`` must appear at the end of the specified part of the web request.
            :param target_string: The value that you want AWS WAF to search for. AWS WAF searches for the specified string in the part of web requests that you specified in ``FieldToMatch`` . The maximum length of the value is 50 bytes. You must specify this property or the ``TargetStringBase64`` property. Valid values depend on the values that you specified for ``FieldToMatch`` : - ``HEADER`` : The value that you want AWS WAF to search for in the request header that you specified in ``FieldToMatch`` , for example, the value of the ``User-Agent`` or ``Referer`` header. - ``METHOD`` : The HTTP method, which indicates the type of operation specified in the request. - ``QUERY_STRING`` : The value that you want AWS WAF to search for in the query string, which is the part of a URL that appears after a ``?`` character. - ``URI`` : The value that you want AWS WAF to search for in the part of a URL that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but instead of inspecting a single parameter, AWS WAF inspects all parameters within the query string for the value or regex pattern that you specify in ``TargetString`` . If ``TargetString`` includes alphabetic characters A-Z and a-z, note that the value is case sensitive.
            :param target_string_base64: The base64-encoded value that AWS WAF searches for. AWS CloudFormation sends this value to AWS WAF without encoding it. You must specify this property or the ``TargetString`` property. AWS WAF searches for this value in a specific part of web requests, which you define in the ``FieldToMatch`` property. Valid values depend on the Type value in the ``FieldToMatch`` property. For example, for a ``METHOD`` type, you must specify HTTP methods such as ``DELETE, GET, HEAD, OPTIONS, PATCH, POST`` , and ``PUT`` .
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value. *NONE* Specify ``NONE`` if you don't want to perform any text transformations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                byte_match_tuple_property = wafregional_mixins.CfnByteMatchSetPropsMixin.ByteMatchTupleProperty(
                    field_to_match=wafregional_mixins.CfnByteMatchSetPropsMixin.FieldToMatchProperty(
                        data="data",
                        type="type"
                    ),
                    positional_constraint="positionalConstraint",
                    target_string="targetString",
                    target_string_base64="targetStringBase64",
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d963847d6f8e762ea73c263ae2c27cb5f237189b04174ad982847a83a7821f35)
                check_type(argname="argument field_to_match", value=field_to_match, expected_type=type_hints["field_to_match"])
                check_type(argname="argument positional_constraint", value=positional_constraint, expected_type=type_hints["positional_constraint"])
                check_type(argname="argument target_string", value=target_string, expected_type=type_hints["target_string"])
                check_type(argname="argument target_string_base64", value=target_string_base64, expected_type=type_hints["target_string_base64"])
                check_type(argname="argument text_transformation", value=text_transformation, expected_type=type_hints["text_transformation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_to_match is not None:
                self._values["field_to_match"] = field_to_match
            if positional_constraint is not None:
                self._values["positional_constraint"] = positional_constraint
            if target_string is not None:
                self._values["target_string"] = target_string
            if target_string_base64 is not None:
                self._values["target_string_base64"] = target_string_base64
            if text_transformation is not None:
                self._values["text_transformation"] = text_transformation

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnByteMatchSetPropsMixin.FieldToMatchProperty"]]:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnByteMatchSetPropsMixin.FieldToMatchProperty"]], result)

        @builtins.property
        def positional_constraint(self) -> typing.Optional[builtins.str]:
            '''Within the portion of a web request that you want to search (for example, in the query string, if any), specify where you want AWS WAF to search.

            Valid values include the following:

            *CONTAINS*

            The specified part of the web request must include the value of ``TargetString`` , but the location doesn't matter.

            *CONTAINS_WORD*

            The specified part of the web request must include the value of ``TargetString`` , and ``TargetString`` must contain only alphanumeric characters or underscore (A-Z, a-z, 0-9, or _). In addition, ``TargetString`` must be a word, which means one of the following:

            - ``TargetString`` exactly matches the value of the specified part of the web request, such as the value of a header.
            - ``TargetString`` is at the beginning of the specified part of the web request and is followed by a character other than an alphanumeric character or underscore (_), for example, ``BadBot;`` .
            - ``TargetString`` is at the end of the specified part of the web request and is preceded by a character other than an alphanumeric character or underscore (_), for example, ``;BadBot`` .
            - ``TargetString`` is in the middle of the specified part of the web request and is preceded and followed by characters other than alphanumeric characters or underscore (_), for example, ``-BadBot;`` .

            *EXACTLY*

            The value of the specified part of the web request must exactly match the value of ``TargetString`` .

            *STARTS_WITH*

            The value of ``TargetString`` must appear at the beginning of the specified part of the web request.

            *ENDS_WITH*

            The value of ``TargetString`` must appear at the end of the specified part of the web request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-positionalconstraint
            '''
            result = self._values.get("positional_constraint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_string(self) -> typing.Optional[builtins.str]:
            '''The value that you want AWS WAF to search for.

            AWS WAF searches for the specified string in the part of web requests that you specified in ``FieldToMatch`` . The maximum length of the value is 50 bytes.

            You must specify this property or the ``TargetStringBase64`` property.

            Valid values depend on the values that you specified for ``FieldToMatch`` :

            - ``HEADER`` : The value that you want AWS WAF to search for in the request header that you specified in ``FieldToMatch`` , for example, the value of the ``User-Agent`` or ``Referer`` header.
            - ``METHOD`` : The HTTP method, which indicates the type of operation specified in the request.
            - ``QUERY_STRING`` : The value that you want AWS WAF to search for in the query string, which is the part of a URL that appears after a ``?`` character.
            - ``URI`` : The value that you want AWS WAF to search for in the part of a URL that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but instead of inspecting a single parameter, AWS WAF inspects all parameters within the query string for the value or regex pattern that you specify in ``TargetString`` .

            If ``TargetString`` includes alphabetic characters A-Z and a-z, note that the value is case sensitive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-targetstring
            '''
            result = self._values.get("target_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_string_base64(self) -> typing.Optional[builtins.str]:
            '''The base64-encoded value that AWS WAF searches for. AWS CloudFormation sends this value to AWS WAF without encoding it.

            You must specify this property or the ``TargetString`` property.

            AWS WAF searches for this value in a specific part of web requests, which you define in the ``FieldToMatch`` property.

            Valid values depend on the Type value in the ``FieldToMatch`` property. For example, for a ``METHOD`` type, you must specify HTTP methods such as ``DELETE, GET, HEAD, OPTIONS, PATCH, POST`` , and ``PUT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-targetstringbase64
            '''
            result = self._values.get("target_string_base64")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_transformation(self) -> typing.Optional[builtins.str]:
            '''Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF .

            If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match.

            You can only specify a single type of TextTransformation.

            *CMD_LINE*

            When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations:

            - Delete the following characters: \\ " ' ^
            - Delete spaces before the following characters: / (
            - Replace the following characters with a space: , ;
            - Replace multiple spaces with one space
            - Convert uppercase letters (A-Z) to lowercase (a-z)

            *COMPRESS_WHITE_SPACE*

            Use this option to replace the following characters with a space character (decimal 32):

            - \\f, formfeed, decimal 12
            - \\t, tab, decimal 9
            - \\n, newline, decimal 10
            - \\r, carriage return, decimal 13
            - \\v, vertical tab, decimal 11
            - non-breaking space, decimal 160

            ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.

            *HTML_ENTITY_DECODE*

            Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations:

            - Replaces ``(ampersand)quot;`` with ``"``
            - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
            - Replaces ``(ampersand)lt;`` with a "less than" symbol
            - Replaces ``(ampersand)gt;`` with ``>``
            - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters
            - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters

            *LOWERCASE*

            Use this option to convert uppercase letters (A-Z) to lowercase (a-z).

            *URL_DECODE*

            Use this option to decode a URL-encoded value.

            *NONE*

            Specify ``NONE`` if you don't want to perform any text transformations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-texttransformation
            '''
            result = self._values.get("text_transformation")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ByteMatchTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnByteMatchSetPropsMixin.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"data": "data", "type": "type"},
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            data: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

            .. epigraph::

               This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies where in a web request to look for ``TargetString`` .

            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .
            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform. - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                field_to_match_property = wafregional_mixins.CfnByteMatchSetPropsMixin.FieldToMatchProperty(
                    data="data",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90914177f8d117a2cf0912e37528bc485d16f60eb89654bfaf18d503eace7f7c)
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data is not None:
                self._values["data"] = data
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` .

            The name of the header is not case sensitive.

            When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive.

            If the value of ``Type`` is any other value, omit ``Data`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-fieldtomatch.html#cfn-wafregional-bytematchset-fieldtomatch-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The part of the web request that you want AWS WAF to search for a specified string.

            Parts of a request that you can search include the following:

            - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` .
            - ``METHOD`` : The HTTP method, which indicated the type of operation that the request is asking the origin to perform.
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-fieldtomatch.html#cfn-wafregional-bytematchset-fieldtomatch-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnGeoMatchSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={"geo_match_constraints": "geoMatchConstraints", "name": "name"},
)
class CfnGeoMatchSetMixinProps:
    def __init__(
        self,
        *,
        geo_match_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGeoMatchSetPropsMixin.GeoMatchConstraintProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGeoMatchSetPropsMixin.

        :param geo_match_constraints: An array of ``GeoMatchConstraint`` objects, which contain the country that you want AWS WAF to search for.
        :param name: A friendly name or description of the ``GeoMatchSet`` . You can't change the name of an ``GeoMatchSet`` after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_geo_match_set_mixin_props = wafregional_mixins.CfnGeoMatchSetMixinProps(
                geo_match_constraints=[wafregional_mixins.CfnGeoMatchSetPropsMixin.GeoMatchConstraintProperty(
                    type="type",
                    value="value"
                )],
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f73015d4764c4880f1f4a749c4de52bb927a9ac5aff242667c06eae89857f25)
            check_type(argname="argument geo_match_constraints", value=geo_match_constraints, expected_type=type_hints["geo_match_constraints"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if geo_match_constraints is not None:
            self._values["geo_match_constraints"] = geo_match_constraints
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def geo_match_constraints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGeoMatchSetPropsMixin.GeoMatchConstraintProperty"]]]]:
        '''An array of ``GeoMatchConstraint`` objects, which contain the country that you want AWS WAF to search for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html#cfn-wafregional-geomatchset-geomatchconstraints
        '''
        result = self._values.get("geo_match_constraints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGeoMatchSetPropsMixin.GeoMatchConstraintProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name or description of the ``GeoMatchSet`` .

        You can't change the name of an ``GeoMatchSet`` after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html#cfn-wafregional-geomatchset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGeoMatchSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGeoMatchSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnGeoMatchSetPropsMixin",
):
    '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    Contains one or more countries that AWS WAF will search for.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-geomatchset.html
    :cloudformationResource: AWS::WAFRegional::GeoMatchSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_geo_match_set_props_mixin = wafregional_mixins.CfnGeoMatchSetPropsMixin(wafregional_mixins.CfnGeoMatchSetMixinProps(
            geo_match_constraints=[wafregional_mixins.CfnGeoMatchSetPropsMixin.GeoMatchConstraintProperty(
                type="type",
                value="value"
            )],
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGeoMatchSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::GeoMatchSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9fd5124be3b97ed644fa8319b7a7d65a655901c6f1570aaa8f683b0b8d12ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea28a21c5293ccf70b4d9f5d63689703357095254a2e42066028c62da79b6dd4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b96da30d83bd7a00c3a94a3fb6ccf4f9d9ea007105fd55f6d4e1ad4fb69e68)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGeoMatchSetMixinProps:
        return typing.cast(CfnGeoMatchSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnGeoMatchSetPropsMixin.GeoMatchConstraintProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class GeoMatchConstraintProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

            .. epigraph::

               This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            The country from which web requests originate that you want AWS WAF to search for.

            :param type: The type of geographical area you want AWS WAF to search for. Currently ``Country`` is the only valid value.
            :param value: The country that you want AWS WAF to search for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-geomatchset-geomatchconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                geo_match_constraint_property = wafregional_mixins.CfnGeoMatchSetPropsMixin.GeoMatchConstraintProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94fe3364659887874256b61571ab8f3b2cdae805ba224a0b6c76739a2413c8f3)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of geographical area you want AWS WAF to search for.

            Currently ``Country`` is the only valid value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-geomatchset-geomatchconstraint.html#cfn-wafregional-geomatchset-geomatchconstraint-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The country that you want AWS WAF to search for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-geomatchset-geomatchconstraint.html#cfn-wafregional-geomatchset-geomatchconstraint-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeoMatchConstraintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnIPSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={"ip_set_descriptors": "ipSetDescriptors", "name": "name"},
)
class CfnIPSetMixinProps:
    def __init__(
        self,
        *,
        ip_set_descriptors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIPSetPropsMixin.IPSetDescriptorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIPSetPropsMixin.

        :param ip_set_descriptors: The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from.
        :param name: A friendly name or description of the ``IPSet`` . You can't change the name of an ``IPSet`` after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_iPSet_mixin_props = wafregional_mixins.CfnIPSetMixinProps(
                ip_set_descriptors=[{
                    "type": "type",
                    "value": "value"
                }],
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__babd7cfbb69f0b653a1e24b5ac9a3648e2bcff937cac0224336e31e246e4f194)
            check_type(argname="argument ip_set_descriptors", value=ip_set_descriptors, expected_type=type_hints["ip_set_descriptors"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip_set_descriptors is not None:
            self._values["ip_set_descriptors"] = ip_set_descriptors
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def ip_set_descriptors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIPSetPropsMixin.IPSetDescriptorProperty"]]]]:
        '''The IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR notation) that web requests originate from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html#cfn-wafregional-ipset-ipsetdescriptors
        '''
        result = self._values.get("ip_set_descriptors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIPSetPropsMixin.IPSetDescriptorProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name or description of the ``IPSet`` .

        You can't change the name of an ``IPSet`` after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html#cfn-wafregional-ipset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIPSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIPSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnIPSetPropsMixin",
):
    '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    Contains one or more IP addresses or blocks of IP addresses specified in Classless Inter-Domain Routing (CIDR) notation. AWS WAF supports IPv4 address ranges: /8 and any range between /16 through /32. AWS WAF supports IPv6 address ranges: /24, /32, /48, /56, /64, and /128.

    To specify an individual IP address, you specify the four-part IP address followed by a ``/32`` , for example, 192.0.2.0/32. To block a range of IP addresses, you can specify /8 or any range between /16 through /32 (for IPv4) or /24, /32, /48, /56, /64, or /128 (for IPv6). For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html
    :cloudformationResource: AWS::WAFRegional::IPSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_iPSet_props_mixin = wafregional_mixins.CfnIPSetPropsMixin(wafregional_mixins.CfnIPSetMixinProps(
            ip_set_descriptors=[{
                "type": "type",
                "value": "value"
            }],
            name="name"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIPSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::IPSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a0927fb39a9ae7dc0b39075b446a9022aa337d1afc544c320e0446e489da59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d35c7f81a544b49e360908db2d0f7147e664fd63434a7cc3fe70450788a2d231)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92786ca018c6a19e7dedfbbff9e2e9fd20bdfb41e3604f1abc54a2df1228d73d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIPSetMixinProps:
        return typing.cast(CfnIPSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnIPSetPropsMixin.IPSetDescriptorProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class IPSetDescriptorProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

            .. epigraph::

               This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies the IP address type ( ``IPV4`` or ``IPV6`` ) and the IP address range (in CIDR format) that web requests originate from.

            :param type: Specify ``IPV4`` or ``IPV6`` .
            :param value: Specify an IPv4 address by using CIDR notation. For example:. - To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify ``192.0.2.44/32`` . - To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` . For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ . Specify an IPv6 address by using CIDR notation. For example: - To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` . - To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                i_pSet_descriptor_property = {
                    "type": "type",
                    "value": "value"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd2275bc60a00ae0a66d32fac0f50b919d2a727aa2e439a974707a3d9dca245f)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specify ``IPV4`` or ``IPV6`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html#cfn-wafregional-ipset-ipsetdescriptor-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Specify an IPv4 address by using CIDR notation. For example:.

            - To configure AWS WAF to allow, block, or count requests that originated from the IP address 192.0.2.44, specify ``192.0.2.44/32`` .
            - To configure AWS WAF to allow, block, or count requests that originated from IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` .

            For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            Specify an IPv6 address by using CIDR notation. For example:

            - To configure AWS WAF to allow, block, or count requests that originated from the IP address 1111:0000:0000:0000:0000:0000:0000:0111, specify ``1111:0000:0000:0000:0000:0000:0000:0111/128`` .
            - To configure AWS WAF to allow, block, or count requests that originated from IP addresses 1111:0000:0000:0000:0000:0000:0000:0000 to 1111:0000:0000:0000:ffff:ffff:ffff:ffff, specify ``1111:0000:0000:0000:0000:0000:0000:0000/64`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html#cfn-wafregional-ipset-ipsetdescriptor-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IPSetDescriptorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnRateBasedRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "match_predicates": "matchPredicates",
        "metric_name": "metricName",
        "name": "name",
        "rate_key": "rateKey",
        "rate_limit": "rateLimit",
    },
)
class CfnRateBasedRuleMixinProps:
    def __init__(
        self,
        *,
        match_predicates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRateBasedRulePropsMixin.PredicateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rate_key: typing.Optional[builtins.str] = None,
        rate_limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnRateBasedRulePropsMixin.

        :param match_predicates: The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet>`` object that you want to include in a ``RateBasedRule`` .
        :param metric_name: A name for the metrics for a ``RateBasedRule`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change the name of the metric after you create the ``RateBasedRule`` .
        :param name: A friendly name or description for a ``RateBasedRule`` . You can't change the name of a ``RateBasedRule`` after you create it.
        :param rate_key: The field that AWS WAF uses to determine if requests are likely arriving from single source and thus subject to rate monitoring. The only valid value for ``RateKey`` is ``IP`` . ``IP`` indicates that requests arriving from the same IP address are subject to the ``RateLimit`` that is specified in the ``RateBasedRule`` .
        :param rate_limit: The maximum number of requests, which have an identical value in the field specified by the ``RateKey`` , allowed in a five-minute period. If the number of requests exceeds the ``RateLimit`` and the other predicates specified in the rule are also met, AWS WAF triggers the action that is specified for this rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_rate_based_rule_mixin_props = wafregional_mixins.CfnRateBasedRuleMixinProps(
                match_predicates=[wafregional_mixins.CfnRateBasedRulePropsMixin.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )],
                metric_name="metricName",
                name="name",
                rate_key="rateKey",
                rate_limit=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85db7f38535a8c95ba5d3ddd72b82868720edc98a1cdd349837247154cd4abca)
            check_type(argname="argument match_predicates", value=match_predicates, expected_type=type_hints["match_predicates"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rate_key", value=rate_key, expected_type=type_hints["rate_key"])
            check_type(argname="argument rate_limit", value=rate_limit, expected_type=type_hints["rate_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if match_predicates is not None:
            self._values["match_predicates"] = match_predicates
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if name is not None:
            self._values["name"] = name
        if rate_key is not None:
            self._values["rate_key"] = rate_key
        if rate_limit is not None:
            self._values["rate_limit"] = rate_limit

    @builtins.property
    def match_predicates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRateBasedRulePropsMixin.PredicateProperty"]]]]:
        '''The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet>`` object that you want to include in a ``RateBasedRule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-matchpredicates
        '''
        result = self._values.get("match_predicates")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRateBasedRulePropsMixin.PredicateProperty"]]]], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''A name for the metrics for a ``RateBasedRule`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF , including "All" and "Default_Action." You can't change the name of the metric after you create the ``RateBasedRule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-metricname
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name or description for a ``RateBasedRule`` .

        You can't change the name of a ``RateBasedRule`` after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_key(self) -> typing.Optional[builtins.str]:
        '''The field that AWS WAF uses to determine if requests are likely arriving from single source and thus subject to rate monitoring.

        The only valid value for ``RateKey`` is ``IP`` . ``IP`` indicates that requests arriving from the same IP address are subject to the ``RateLimit`` that is specified in the ``RateBasedRule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-ratekey
        '''
        result = self._values.get("rate_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rate_limit(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of requests, which have an identical value in the field specified by the ``RateKey`` , allowed in a five-minute period.

        If the number of requests exceeds the ``RateLimit`` and the other predicates specified in the rule are also met, AWS WAF triggers the action that is specified for this rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html#cfn-wafregional-ratebasedrule-ratelimit
        '''
        result = self._values.get("rate_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRateBasedRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRateBasedRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnRateBasedRulePropsMixin",
):
    '''.. epigraph::

   This is *AWS WAF Classic* documentation.

    For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
    .. epigraph::

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A ``RateBasedRule`` is identical to a regular ``Rule`` , with one addition: a ``RateBasedRule`` counts the number of requests that arrive from a specified IP address every five minutes. For example, based on recent requests that you've seen from an attacker, you might create a ``RateBasedRule`` that includes the following conditions:

    - The requests come from 192.0.2.44.
    - They contain the value ``BadBot`` in the ``User-Agent`` header.

    In the rule, you also define the rate limit as 15,000.

    Requests that meet both of these conditions and exceed 15,000 requests every five minutes trigger the rule's action (block or count), which is defined in the web ACL.

    Note you can only create rate-based rules using an CloudFormation template. To add the rate-based rules created through CloudFormation to a web ACL, use the AWS WAF console, API, or command line interface (CLI). For more information, see `UpdateWebACL <https://docs.aws.amazon.com/waf/latest/APIReference/API_regional_UpdateWebACL.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ratebasedrule.html
    :cloudformationResource: AWS::WAFRegional::RateBasedRule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_rate_based_rule_props_mixin = wafregional_mixins.CfnRateBasedRulePropsMixin(wafregional_mixins.CfnRateBasedRuleMixinProps(
            match_predicates=[wafregional_mixins.CfnRateBasedRulePropsMixin.PredicateProperty(
                data_id="dataId",
                negated=False,
                type="type"
            )],
            metric_name="metricName",
            name="name",
            rate_key="rateKey",
            rate_limit=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRateBasedRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::RateBasedRule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__184f6611c1e592feebb954d826b04473ca86e0aa063906d39bf161688547046c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0a54332626b6c6d4ed1ab5580ae8bdcfb0c8efb77b67ca53d35f7c60f8e2386)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f42748979182ec36d6b760ea98dbc5c13ffe9fb7457e995e380c4b46478d12)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRateBasedRuleMixinProps:
        return typing.cast(CfnRateBasedRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnRateBasedRulePropsMixin.PredicateProperty",
        jsii_struct_bases=[],
        name_mapping={"data_id": "dataId", "negated": "negated", "type": "type"},
    )
    class PredicateProperty:
        def __init__(
            self,
            *,
            data_id: typing.Optional[builtins.str] = None,
            negated: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , and ``SizeConstraintSet`` objects that you want to add to a ``Rule`` and, for each object, indicates whether you want to negate the settings, for example, requests that do NOT originate from the IP address 192.0.2.44.

            :param data_id: A unique identifier for a predicate in a ``Rule`` , such as ``ByteMatchSetId`` or ``IPSetId`` . The ID is returned by the corresponding ``Create`` or ``List`` command.
            :param negated: Set ``Negated`` to ``False`` if you want AWS WAF to allow, block, or count requests based on the settings in the specified ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` . For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow or block requests based on that IP address. Set ``Negated`` to ``True`` if you want AWS WAF to allow or block a request based on the negation of the settings in the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` >. For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow, block, or count requests based on all IP addresses *except* ``192.0.2.44`` .
            :param type: The type of predicate in a ``Rule`` , such as ``ByteMatch`` or ``IPSet`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ratebasedrule-predicate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                predicate_property = wafregional_mixins.CfnRateBasedRulePropsMixin.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__148707adfce5a96d55db9455f9545e29a2ae4d3b28aebecdede1fb612a7214af)
                check_type(argname="argument data_id", value=data_id, expected_type=type_hints["data_id"])
                check_type(argname="argument negated", value=negated, expected_type=type_hints["negated"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_id is not None:
                self._values["data_id"] = data_id
            if negated is not None:
                self._values["negated"] = negated
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def data_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for a predicate in a ``Rule`` , such as ``ByteMatchSetId`` or ``IPSetId`` .

            The ID is returned by the corresponding ``Create`` or ``List`` command.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ratebasedrule-predicate.html#cfn-wafregional-ratebasedrule-predicate-dataid
            '''
            result = self._values.get("data_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def negated(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set ``Negated`` to ``False`` if you want AWS WAF to allow, block, or count requests based on the settings in the specified ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` .

            For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow or block requests based on that IP address.

            Set ``Negated`` to ``True`` if you want AWS WAF to allow or block a request based on the negation of the settings in the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` >. For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow, block, or count requests based on all IP addresses *except* ``192.0.2.44`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ratebasedrule-predicate.html#cfn-wafregional-ratebasedrule-predicate-negated
            '''
            result = self._values.get("negated")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of predicate in a ``Rule`` , such as ``ByteMatch`` or ``IPSet`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ratebasedrule-predicate.html#cfn-wafregional-ratebasedrule-predicate-type
            '''
            result = self._values.get("type")
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
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnRegexPatternSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "regex_pattern_strings": "regexPatternStrings"},
)
class CfnRegexPatternSetMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        regex_pattern_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnRegexPatternSetPropsMixin.

        :param name: A friendly name or description of the ``RegexPatternSet`` . You can't change ``Name`` after you create a ``RegexPatternSet`` .
        :param regex_pattern_strings: Specifies the regular expression (regex) patterns that you want AWS WAF to search for, such as ``B[a@]dB[o0]t`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_regex_pattern_set_mixin_props = wafregional_mixins.CfnRegexPatternSetMixinProps(
                name="name",
                regex_pattern_strings=["regexPatternStrings"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1970cc3cddd4130e60d3bec941a12dc196ae64dac8cd269ae5f165a7881841bf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument regex_pattern_strings", value=regex_pattern_strings, expected_type=type_hints["regex_pattern_strings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if regex_pattern_strings is not None:
            self._values["regex_pattern_strings"] = regex_pattern_strings

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name or description of the ``RegexPatternSet`` .

        You can't change ``Name`` after you create a ``RegexPatternSet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html#cfn-wafregional-regexpatternset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex_pattern_strings(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the regular expression (regex) patterns that you want AWS WAF to search for, such as ``B[a@]dB[o0]t`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html#cfn-wafregional-regexpatternset-regexpatternstrings
        '''
        result = self._values.get("regex_pattern_strings")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRegexPatternSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRegexPatternSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnRegexPatternSetPropsMixin",
):
    '''The ``RegexPatternSet`` specifies the regular expression (regex) pattern that you want AWS WAF to search for, such as ``B[a@]dB[o0]t`` .

    You can then configure AWS WAF to reject those requests.

    Note that you can only create regex pattern sets using a CloudFormation template. To add the regex pattern sets created through CloudFormation to a RegexMatchSet, use the AWS WAF console, API, or command line interface (CLI). For more information, see `UpdateRegexMatchSet <https://docs.aws.amazon.com/waf/latest/APIReference/API_regional_UpdateRegexMatchSet.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-regexpatternset.html
    :cloudformationResource: AWS::WAFRegional::RegexPatternSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_regex_pattern_set_props_mixin = wafregional_mixins.CfnRegexPatternSetPropsMixin(wafregional_mixins.CfnRegexPatternSetMixinProps(
            name="name",
            regex_pattern_strings=["regexPatternStrings"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRegexPatternSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::RegexPatternSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8219df53ccacfc3e3ee964955901eda2e6626248cca340baa7e0531d7987942d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1125c95537792d331feb8ab24e34df7646ea9e864251706f306604a0239c853b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f642691e2641ebdddfba2635336ffcbe5f824dd1da44a27087e4813b06ec401c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRegexPatternSetMixinProps:
        return typing.cast(CfnRegexPatternSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "metric_name": "metricName",
        "name": "name",
        "predicates": "predicates",
    },
)
class CfnRuleMixinProps:
    def __init__(
        self,
        *,
        metric_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        predicates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.PredicateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnRulePropsMixin.

        :param metric_name: A name for the metrics for this ``Rule`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .
        :param name: The friendly name or description for the ``Rule`` . You can't change the name of a ``Rule`` after you create it.
        :param predicates: The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_rule_mixin_props = wafregional_mixins.CfnRuleMixinProps(
                metric_name="metricName",
                name="name",
                predicates=[wafregional_mixins.CfnRulePropsMixin.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0cfd0ef69882f962de27979ba8e34d6cf4577a583cd1e2ffc76ae11c97022a)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument predicates", value=predicates, expected_type=type_hints["predicates"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if name is not None:
            self._values["name"] = name
        if predicates is not None:
            self._values["predicates"] = predicates

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''A name for the metrics for this ``Rule`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``Rule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-metricname
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The friendly name or description for the ``Rule`` .

        You can't change the name of a ``Rule`` after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predicates(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.PredicateProperty"]]]]:
        '''The ``Predicates`` object contains one ``Predicate`` element for each ``ByteMatchSet`` , ``IPSet`` , or ``SqlInjectionMatchSet`` object that you want to include in a ``Rule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-predicates
        '''
        result = self._values.get("predicates")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.PredicateProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnRulePropsMixin",
):
    '''.. epigraph::

   This is *AWS WAF Classic* documentation.

    For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
    .. epigraph::

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A combination of ``ByteMatchSet`` , ``IPSet`` , and/or ``SqlInjectionMatchSet`` objects that identify the web requests that you want to allow, block, or count. For example, you might create a ``Rule`` that includes the following predicates:

    - An ``IPSet`` that causes AWS WAF to search for web requests that originate from the IP address ``192.0.2.44``
    - A ``ByteMatchSet`` that causes AWS WAF to search for web requests for which the value of the ``User-Agent`` header is ``BadBot`` .

    To match the settings in this ``Rule`` , a request must originate from ``192.0.2.44`` AND include a ``User-Agent`` header for which the value is ``BadBot`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html
    :cloudformationResource: AWS::WAFRegional::Rule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_rule_props_mixin = wafregional_mixins.CfnRulePropsMixin(wafregional_mixins.CfnRuleMixinProps(
            metric_name="metricName",
            name="name",
            predicates=[wafregional_mixins.CfnRulePropsMixin.PredicateProperty(
                data_id="dataId",
                negated=False,
                type="type"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::Rule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b22d929b80ef8fb9fb2a92a21ccb1249a24c96c715783a12036bd2ee68d15b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29600b91d56c8ead7c704e1cab82041c31cd8572d9f2044ea44ff3a0affd489d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36f38b8cd5a2242d62c3d9472c20b65b502f31a19981fcaaa62bd7d8055eb48)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRuleMixinProps:
        return typing.cast(CfnRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnRulePropsMixin.PredicateProperty",
        jsii_struct_bases=[],
        name_mapping={"data_id": "dataId", "negated": "negated", "type": "type"},
    )
    class PredicateProperty:
        def __init__(
            self,
            *,
            data_id: typing.Optional[builtins.str] = None,
            negated: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , and ``SizeConstraintSet`` objects that you want to add to a ``Rule`` and, for each object, indicates whether you want to negate the settings, for example, requests that do NOT originate from the IP address 192.0.2.44.

            :param data_id: A unique identifier for a predicate in a ``Rule`` , such as ``ByteMatchSetId`` or ``IPSetId`` . The ID is returned by the corresponding ``Create`` or ``List`` command.
            :param negated: Set ``Negated`` to ``False`` if you want AWS WAF to allow, block, or count requests based on the settings in the specified ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` . For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow or block requests based on that IP address. Set ``Negated`` to ``True`` if you want AWS WAF to allow or block a request based on the negation of the settings in the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` . For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow, block, or count requests based on all IP addresses *except* ``192.0.2.44`` .
            :param type: The type of predicate in a ``Rule`` , such as ``ByteMatch`` or ``IPSet`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                predicate_property = wafregional_mixins.CfnRulePropsMixin.PredicateProperty(
                    data_id="dataId",
                    negated=False,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__47392c5cb06519699ebd0ff40176035920f8afb40e23f048929c44ea1efa9aa7)
                check_type(argname="argument data_id", value=data_id, expected_type=type_hints["data_id"])
                check_type(argname="argument negated", value=negated, expected_type=type_hints["negated"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_id is not None:
                self._values["data_id"] = data_id
            if negated is not None:
                self._values["negated"] = negated
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def data_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for a predicate in a ``Rule`` , such as ``ByteMatchSetId`` or ``IPSetId`` .

            The ID is returned by the corresponding ``Create`` or ``List`` command.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html#cfn-wafregional-rule-predicate-dataid
            '''
            result = self._values.get("data_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def negated(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set ``Negated`` to ``False`` if you want AWS WAF to allow, block, or count requests based on the settings in the specified ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` .

            For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow or block requests based on that IP address.

            Set ``Negated`` to ``True`` if you want AWS WAF to allow or block a request based on the negation of the settings in the ``ByteMatchSet`` , ``IPSet`` , ``SqlInjectionMatchSet`` , ``XssMatchSet`` , ``RegexMatchSet`` , ``GeoMatchSet`` , or ``SizeConstraintSet`` . For example, if an ``IPSet`` includes the IP address ``192.0.2.44`` , AWS WAF will allow, block, or count requests based on all IP addresses *except* ``192.0.2.44`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html#cfn-wafregional-rule-predicate-negated
            '''
            result = self._values.get("negated")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of predicate in a ``Rule`` , such as ``ByteMatch`` or ``IPSet`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html#cfn-wafregional-rule-predicate-type
            '''
            result = self._values.get("type")
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
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnSizeConstraintSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "size_constraints": "sizeConstraints"},
)
class CfnSizeConstraintSetMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        size_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSizeConstraintSetPropsMixin.SizeConstraintProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnSizeConstraintSetPropsMixin.

        :param name: The name, if any, of the ``SizeConstraintSet`` .
        :param size_constraints: The size constraint and the part of the web request to check.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_size_constraint_set_mixin_props = wafregional_mixins.CfnSizeConstraintSetMixinProps(
                name="name",
                size_constraints=[wafregional_mixins.CfnSizeConstraintSetPropsMixin.SizeConstraintProperty(
                    comparison_operator="comparisonOperator",
                    field_to_match=wafregional_mixins.CfnSizeConstraintSetPropsMixin.FieldToMatchProperty(
                        data="data",
                        type="type"
                    ),
                    size=123,
                    text_transformation="textTransformation"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c44329f6354e4b699bf1a016d654ffc03a708fcab0a728214de9d5ca35bacc2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument size_constraints", value=size_constraints, expected_type=type_hints["size_constraints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if size_constraints is not None:
            self._values["size_constraints"] = size_constraints

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name, if any, of the ``SizeConstraintSet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html#cfn-wafregional-sizeconstraintset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_constraints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSizeConstraintSetPropsMixin.SizeConstraintProperty"]]]]:
        '''The size constraint and the part of the web request to check.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html#cfn-wafregional-sizeconstraintset-sizeconstraints
        '''
        result = self._values.get("size_constraints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSizeConstraintSetPropsMixin.SizeConstraintProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSizeConstraintSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSizeConstraintSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnSizeConstraintSetPropsMixin",
):
    '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A complex type that contains ``SizeConstraint`` objects, which specify the parts of web requests that you want AWS WAF to inspect the size of. If a ``SizeConstraintSet`` contains more than one ``SizeConstraint`` object, a request only needs to match one constraint to be considered a match.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html
    :cloudformationResource: AWS::WAFRegional::SizeConstraintSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_size_constraint_set_props_mixin = wafregional_mixins.CfnSizeConstraintSetPropsMixin(wafregional_mixins.CfnSizeConstraintSetMixinProps(
            name="name",
            size_constraints=[wafregional_mixins.CfnSizeConstraintSetPropsMixin.SizeConstraintProperty(
                comparison_operator="comparisonOperator",
                field_to_match=wafregional_mixins.CfnSizeConstraintSetPropsMixin.FieldToMatchProperty(
                    data="data",
                    type="type"
                ),
                size=123,
                text_transformation="textTransformation"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSizeConstraintSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::SizeConstraintSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070770dd93457e0d5c726bf76eccc7645bf18ccbeb09e0af2ea8e26c4af2f1ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da557ffcf09708cfcc8161955d4da1b1e53b052b046c467171f80bf9e292c422)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd2ae92efe810326fc9436dea3ee63789bce1631213045a6ed4c89b5e7c7bc4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSizeConstraintSetMixinProps:
        return typing.cast(CfnSizeConstraintSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnSizeConstraintSetPropsMixin.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"data": "data", "type": "type"},
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            data: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .
            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform. - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                field_to_match_property = wafregional_mixins.CfnSizeConstraintSetPropsMixin.FieldToMatchProperty(
                    data="data",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5effb2ddf07e3e14cbaa4ab92c82d5608c24f13bcc278dc6117f81de39ea2957)
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data is not None:
                self._values["data"] = data
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` .

            The name of the header is not case sensitive.

            When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive.

            If the value of ``Type`` is any other value, omit ``Data`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-fieldtomatch.html#cfn-wafregional-sizeconstraintset-fieldtomatch-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The part of the web request that you want AWS WAF to search for a specified string.

            Parts of a request that you can search include the following:

            - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` .
            - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform.
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-fieldtomatch.html#cfn-wafregional-sizeconstraintset-fieldtomatch-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnSizeConstraintSetPropsMixin.SizeConstraintProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "field_to_match": "fieldToMatch",
            "size": "size",
            "text_transformation": "textTransformation",
        },
    )
    class SizeConstraintProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            field_to_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSizeConstraintSetPropsMixin.FieldToMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            size: typing.Optional[jsii.Number] = None,
            text_transformation: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

            .. epigraph::

               This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies a constraint on the size of a part of the web request. AWS WAF uses the ``Size`` , ``ComparisonOperator`` , and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match.

            :param comparison_operator: The type of comparison you want AWS WAF to perform. AWS WAF uses this in combination with the provided ``Size`` and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match. *EQ* : Used to test if the ``Size`` is equal to the size of the ``FieldToMatch`` *NE* : Used to test if the ``Size`` is not equal to the size of the ``FieldToMatch`` *LE* : Used to test if the ``Size`` is less than or equal to the size of the ``FieldToMatch`` *LT* : Used to test if the ``Size`` is strictly less than the size of the ``FieldToMatch`` *GE* : Used to test if the ``Size`` is greater than or equal to the size of the ``FieldToMatch`` *GT* : Used to test if the ``Size`` is strictly greater than the size of the ``FieldToMatch``
            :param field_to_match: The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.
            :param size: The size in bytes that you want AWS WAF to compare against the size of the specified ``FieldToMatch`` . AWS WAF uses this in combination with ``ComparisonOperator`` and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match. Valid values for size are 0 - 21474836480 bytes (0 - 20 GB). If you specify ``URI`` for the value of ``Type`` , the / in the URI path that you specify counts as one character. For example, the URI ``/logo.jpg`` is nine characters long.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting a request for a match. You can only specify a single type of TextTransformation. Note that if you choose ``BODY`` for the value of ``Type`` , you must choose ``NONE`` for ``TextTransformation`` because the API Gateway API or Application Load Balancer forward only the first 8192 bytes for inspection. *NONE* Specify ``NONE`` if you don't want to perform any text transformations. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                size_constraint_property = wafregional_mixins.CfnSizeConstraintSetPropsMixin.SizeConstraintProperty(
                    comparison_operator="comparisonOperator",
                    field_to_match=wafregional_mixins.CfnSizeConstraintSetPropsMixin.FieldToMatchProperty(
                        data="data",
                        type="type"
                    ),
                    size=123,
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__638eda145071ae0eaff85c46c958625fad6cf9db070d7aee0ee2f8e5aa5b09a0)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument field_to_match", value=field_to_match, expected_type=type_hints["field_to_match"])
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                check_type(argname="argument text_transformation", value=text_transformation, expected_type=type_hints["text_transformation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if field_to_match is not None:
                self._values["field_to_match"] = field_to_match
            if size is not None:
                self._values["size"] = size
            if text_transformation is not None:
                self._values["text_transformation"] = text_transformation

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''The type of comparison you want AWS WAF to perform.

            AWS WAF uses this in combination with the provided ``Size`` and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match.

            *EQ* : Used to test if the ``Size`` is equal to the size of the ``FieldToMatch``

            *NE* : Used to test if the ``Size`` is not equal to the size of the ``FieldToMatch``

            *LE* : Used to test if the ``Size`` is less than or equal to the size of the ``FieldToMatch``

            *LT* : Used to test if the ``Size`` is strictly less than the size of the ``FieldToMatch``

            *GE* : Used to test if the ``Size`` is greater than or equal to the size of the ``FieldToMatch``

            *GT* : Used to test if the ``Size`` is strictly greater than the size of the ``FieldToMatch``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSizeConstraintSetPropsMixin.FieldToMatchProperty"]]:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSizeConstraintSetPropsMixin.FieldToMatchProperty"]], result)

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''The size in bytes that you want AWS WAF to compare against the size of the specified ``FieldToMatch`` .

            AWS WAF uses this in combination with ``ComparisonOperator`` and ``FieldToMatch`` to build an expression in the form of " ``Size`` ``ComparisonOperator`` size in bytes of ``FieldToMatch`` ". If that expression is true, the ``SizeConstraint`` is considered to match.

            Valid values for size are 0 - 21474836480 bytes (0 - 20 GB).

            If you specify ``URI`` for the value of ``Type`` , the / in the URI path that you specify counts as one character. For example, the URI ``/logo.jpg`` is nine characters long.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def text_transformation(self) -> typing.Optional[builtins.str]:
            '''Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF .

            If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting a request for a match.

            You can only specify a single type of TextTransformation.

            Note that if you choose ``BODY`` for the value of ``Type`` , you must choose ``NONE`` for ``TextTransformation`` because the API Gateway API or Application Load Balancer forward only the first 8192 bytes for inspection.

            *NONE*

            Specify ``NONE`` if you don't want to perform any text transformations.

            *CMD_LINE*

            When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations:

            - Delete the following characters: \\ " ' ^
            - Delete spaces before the following characters: / (
            - Replace the following characters with a space: , ;
            - Replace multiple spaces with one space
            - Convert uppercase letters (A-Z) to lowercase (a-z)

            *COMPRESS_WHITE_SPACE*

            Use this option to replace the following characters with a space character (decimal 32):

            - \\f, formfeed, decimal 12
            - \\t, tab, decimal 9
            - \\n, newline, decimal 10
            - \\r, carriage return, decimal 13
            - \\v, vertical tab, decimal 11
            - non-breaking space, decimal 160

            ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.

            *HTML_ENTITY_DECODE*

            Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations:

            - Replaces ``(ampersand)quot;`` with ``"``
            - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
            - Replaces ``(ampersand)lt;`` with a "less than" symbol
            - Replaces ``(ampersand)gt;`` with ``>``
            - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters
            - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters

            *LOWERCASE*

            Use this option to convert uppercase letters (A-Z) to lowercase (a-z).

            *URL_DECODE*

            Use this option to decode a URL-encoded value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-texttransformation
            '''
            result = self._values.get("text_transformation")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SizeConstraintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnSqlInjectionMatchSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "sql_injection_match_tuples": "sqlInjectionMatchTuples",
    },
)
class CfnSqlInjectionMatchSetMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        sql_injection_match_tuples: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSqlInjectionMatchSetPropsMixin.SqlInjectionMatchTupleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnSqlInjectionMatchSetPropsMixin.

        :param name: The name, if any, of the ``SqlInjectionMatchSet`` .
        :param sql_injection_match_tuples: Specifies the parts of web requests that you want to inspect for snippets of malicious SQL code.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_sql_injection_match_set_mixin_props = wafregional_mixins.CfnSqlInjectionMatchSetMixinProps(
                name="name",
                sql_injection_match_tuples=[wafregional_mixins.CfnSqlInjectionMatchSetPropsMixin.SqlInjectionMatchTupleProperty(
                    field_to_match=wafregional_mixins.CfnSqlInjectionMatchSetPropsMixin.FieldToMatchProperty(
                        data="data",
                        type="type"
                    ),
                    text_transformation="textTransformation"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ccdacc71c655d8c4c6e61e00edb3de3fab3f1bee3105b20a33eff5c7a101474)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql_injection_match_tuples", value=sql_injection_match_tuples, expected_type=type_hints["sql_injection_match_tuples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if sql_injection_match_tuples is not None:
            self._values["sql_injection_match_tuples"] = sql_injection_match_tuples

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name, if any, of the ``SqlInjectionMatchSet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html#cfn-wafregional-sqlinjectionmatchset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_injection_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSqlInjectionMatchSetPropsMixin.SqlInjectionMatchTupleProperty"]]]]:
        '''Specifies the parts of web requests that you want to inspect for snippets of malicious SQL code.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuples
        '''
        result = self._values.get("sql_injection_match_tuples")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSqlInjectionMatchSetPropsMixin.SqlInjectionMatchTupleProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSqlInjectionMatchSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSqlInjectionMatchSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnSqlInjectionMatchSetPropsMixin",
):
    '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A complex type that contains ``SqlInjectionMatchTuple`` objects, which specify the parts of web requests that you want AWS WAF to inspect for snippets of malicious SQL code and, if you want AWS WAF to inspect a header, the name of the header. If a ``SqlInjectionMatchSet`` contains more than one ``SqlInjectionMatchTuple`` object, a request needs to include snippets of SQL code in only one of the specified parts of the request to be considered a match.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html
    :cloudformationResource: AWS::WAFRegional::SqlInjectionMatchSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_sql_injection_match_set_props_mixin = wafregional_mixins.CfnSqlInjectionMatchSetPropsMixin(wafregional_mixins.CfnSqlInjectionMatchSetMixinProps(
            name="name",
            sql_injection_match_tuples=[wafregional_mixins.CfnSqlInjectionMatchSetPropsMixin.SqlInjectionMatchTupleProperty(
                field_to_match=wafregional_mixins.CfnSqlInjectionMatchSetPropsMixin.FieldToMatchProperty(
                    data="data",
                    type="type"
                ),
                text_transformation="textTransformation"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSqlInjectionMatchSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::SqlInjectionMatchSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab6e2ff37fd5854cdca1edbca1ec590f2eb8c1ca2784acba24c8e4a414604c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2c1842242fa0488400263a578b0804054c3734a7e25a923947c46b73f53ead)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdac36f2b9d540005a8ebd43bd6f1c34cf19187300d621325c84d48811585ea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSqlInjectionMatchSetMixinProps:
        return typing.cast(CfnSqlInjectionMatchSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnSqlInjectionMatchSetPropsMixin.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"data": "data", "type": "type"},
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            data: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .
            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform. - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                field_to_match_property = wafregional_mixins.CfnSqlInjectionMatchSetPropsMixin.FieldToMatchProperty(
                    data="data",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e47a639a2145147294034aa5b29770c07b7badb17387bad69ef166dda9c27d20)
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data is not None:
                self._values["data"] = data
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` .

            The name of the header is not case sensitive.

            When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive.

            If the value of ``Type`` is any other value, omit ``Data`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-fieldtomatch.html#cfn-wafregional-sqlinjectionmatchset-fieldtomatch-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The part of the web request that you want AWS WAF to search for a specified string.

            Parts of a request that you can search include the following:

            - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` .
            - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform.
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-fieldtomatch.html#cfn-wafregional-sqlinjectionmatchset-fieldtomatch-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnSqlInjectionMatchSetPropsMixin.SqlInjectionMatchTupleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "text_transformation": "textTransformation",
        },
    )
    class SqlInjectionMatchTupleProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSqlInjectionMatchSetPropsMixin.FieldToMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            text_transformation: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

            .. epigraph::

               This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies the part of a web request that you want AWS WAF to inspect for snippets of malicious SQL code and, if you want AWS WAF to inspect a header, the name of the header.

            :param field_to_match: The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value. *NONE* Specify ``NONE`` if you don't want to perform any text transformations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                sql_injection_match_tuple_property = wafregional_mixins.CfnSqlInjectionMatchSetPropsMixin.SqlInjectionMatchTupleProperty(
                    field_to_match=wafregional_mixins.CfnSqlInjectionMatchSetPropsMixin.FieldToMatchProperty(
                        data="data",
                        type="type"
                    ),
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f77044b71f7e48a2d3dfc817d6adcaa27cd5d15bd06c9bf6ce53b81f982b3437)
                check_type(argname="argument field_to_match", value=field_to_match, expected_type=type_hints["field_to_match"])
                check_type(argname="argument text_transformation", value=text_transformation, expected_type=type_hints["text_transformation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_to_match is not None:
                self._values["field_to_match"] = field_to_match
            if text_transformation is not None:
                self._values["text_transformation"] = text_transformation

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSqlInjectionMatchSetPropsMixin.FieldToMatchProperty"]]:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSqlInjectionMatchSetPropsMixin.FieldToMatchProperty"]], result)

        @builtins.property
        def text_transformation(self) -> typing.Optional[builtins.str]:
            '''Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF .

            If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match.

            You can only specify a single type of TextTransformation.

            *CMD_LINE*

            When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations:

            - Delete the following characters: \\ " ' ^
            - Delete spaces before the following characters: / (
            - Replace the following characters with a space: , ;
            - Replace multiple spaces with one space
            - Convert uppercase letters (A-Z) to lowercase (a-z)

            *COMPRESS_WHITE_SPACE*

            Use this option to replace the following characters with a space character (decimal 32):

            - \\f, formfeed, decimal 12
            - \\t, tab, decimal 9
            - \\n, newline, decimal 10
            - \\r, carriage return, decimal 13
            - \\v, vertical tab, decimal 11
            - non-breaking space, decimal 160

            ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.

            *HTML_ENTITY_DECODE*

            Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations:

            - Replaces ``(ampersand)quot;`` with ``"``
            - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
            - Replaces ``(ampersand)lt;`` with a "less than" symbol
            - Replaces ``(ampersand)gt;`` with ``>``
            - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters
            - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters

            *LOWERCASE*

            Use this option to convert uppercase letters (A-Z) to lowercase (a-z).

            *URL_DECODE*

            Use this option to decode a URL-encoded value.

            *NONE*

            Specify ``NONE`` if you don't want to perform any text transformations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple-texttransformation
            '''
            result = self._values.get("text_transformation")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqlInjectionMatchTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnWebACLAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "web_acl_id": "webAclId"},
)
class CfnWebACLAssociationMixinProps:
    def __init__(
        self,
        *,
        resource_arn: typing.Optional[builtins.str] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnWebACLAssociationPropsMixin.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource to protect with the web ACL.
        :param web_acl_id: A unique identifier (ID) for the web ACL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_web_aCLAssociation_mixin_props = wafregional_mixins.CfnWebACLAssociationMixinProps(
                resource_arn="resourceArn",
                web_acl_id="webAclId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff6c23cf07cadd7ef7a6488d0b43874c7576003b9b465347b3099bd57b1d56e)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument web_acl_id", value=web_acl_id, expected_type=type_hints["web_acl_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resource to protect with the web ACL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html#cfn-wafregional-webaclassociation-resourcearn
        '''
        result = self._values.get("resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier (ID) for the web ACL.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html#cfn-wafregional-webaclassociation-webaclid
        '''
        result = self._values.get("web_acl_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebACLAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWebACLAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnWebACLAssociationPropsMixin",
):
    '''.. epigraph::

   This is *AWS WAF Classic* documentation.

    For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
    .. epigraph::

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    The AWS::WAFRegional::WebACLAssociation resource associates an AWS WAF Regional web access control group (ACL) with a resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html
    :cloudformationResource: AWS::WAFRegional::WebACLAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_web_aCLAssociation_props_mixin = wafregional_mixins.CfnWebACLAssociationPropsMixin(wafregional_mixins.CfnWebACLAssociationMixinProps(
            resource_arn="resourceArn",
            web_acl_id="webAclId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWebACLAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::WebACLAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__734e3ece604640e48574e580c8a7184602fd48beccb8feb7992569ac080540bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ffa6bf667cca66447fea504089af7a0feacfd0887ab6678261e4b78212a6bcf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c62ecd7b5c206fb13cb76369c4b66ed1b2e7db0fe661f1574bfab641380c31)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWebACLAssociationMixinProps:
        return typing.cast(CfnWebACLAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnWebACLMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "metric_name": "metricName",
        "name": "name",
        "rules": "rules",
    },
)
class CfnWebACLMixinProps:
    def __init__(
        self,
        *,
        default_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebACLPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        metric_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebACLPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnWebACLPropsMixin.

        :param default_action: The action to perform if none of the ``Rules`` contained in the ``WebACL`` match. The action is specified by the ``WafAction`` object.
        :param metric_name: A name for the metrics for this ``WebACL`` . The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .
        :param name: A friendly name or description of the ``WebACL`` . You can't change the name of a ``WebACL`` after you create it.
        :param rules: An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_web_aCLMixin_props = wafregional_mixins.CfnWebACLMixinProps(
                default_action=wafregional_mixins.CfnWebACLPropsMixin.ActionProperty(
                    type="type"
                ),
                metric_name="metricName",
                name="name",
                rules=[wafregional_mixins.CfnWebACLPropsMixin.RuleProperty(
                    action=wafregional_mixins.CfnWebACLPropsMixin.ActionProperty(
                        type="type"
                    ),
                    priority=123,
                    rule_id="ruleId"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b1aaa9309afc15b64947fa701066c679ac69681b3da83d8f3a3e0695fc0053)
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_action is not None:
            self._values["default_action"] = default_action
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if name is not None:
            self._values["name"] = name
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def default_action(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebACLPropsMixin.ActionProperty"]]:
        '''The action to perform if none of the ``Rules`` contained in the ``WebACL`` match.

        The action is specified by the ``WafAction`` object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-defaultaction
        '''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebACLPropsMixin.ActionProperty"]], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''A name for the metrics for this ``WebACL`` .

        The name can contain only alphanumeric characters (A-Z, a-z, 0-9), with maximum length 128 and minimum length one. It can't contain whitespace or metric names reserved for AWS WAF, including "All" and "Default_Action." You can't change ``MetricName`` after you create the ``WebACL`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-metricname
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name or description of the ``WebACL`` .

        You can't change the name of a ``WebACL`` after you create it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebACLPropsMixin.RuleProperty"]]]]:
        '''An array that contains the action for each ``Rule`` in a ``WebACL`` , the priority of the ``Rule`` , and the ID of the ``Rule`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebACLPropsMixin.RuleProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebACLMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWebACLPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnWebACLPropsMixin",
):
    '''.. epigraph::

   This is *AWS WAF Classic* documentation.

    For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.
    .. epigraph::

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    Contains the ``Rules`` that identify the requests that you want to allow, block, or count. In a ``WebACL`` , you also specify a default action ( ``ALLOW`` or ``BLOCK`` ), and the action for each ``Rule`` that you add to a ``WebACL`` , for example, block requests from specified IP addresses or block requests from specified referrers. If you add more than one ``Rule`` to a ``WebACL`` , a request needs to match only one of the specifications to be allowed, blocked, or counted.

    To identify the requests that you want AWS WAF to filter, you associate the ``WebACL`` with an API Gateway API or an Application Load Balancer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html
    :cloudformationResource: AWS::WAFRegional::WebACL
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_web_aCLProps_mixin = wafregional_mixins.CfnWebACLPropsMixin(wafregional_mixins.CfnWebACLMixinProps(
            default_action=wafregional_mixins.CfnWebACLPropsMixin.ActionProperty(
                type="type"
            ),
            metric_name="metricName",
            name="name",
            rules=[wafregional_mixins.CfnWebACLPropsMixin.RuleProperty(
                action=wafregional_mixins.CfnWebACLPropsMixin.ActionProperty(
                    type="type"
                ),
                priority=123,
                rule_id="ruleId"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWebACLMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::WebACL``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8847394a1350ffd1a77aacf08a6c5357cc9134025e3d2c604ef7222f1631aed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf0deafe468468c337c9eb0970caac6de5c2888f34a00c3831c4bc0ca22501a4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25984fd39de7ad1eb8f2215a94a81246453797a3067c963cb0a26a2270dcb2fb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWebACLMixinProps:
        return typing.cast(CfnWebACLMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnWebACLPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class ActionProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the action AWS WAF takes when a web request matches or doesn't match all rule conditions.

            :param type: For actions that are associated with a rule, the action that AWS WAF takes when a web request matches all conditions in a rule. For the default action of a web access control list (ACL), the action that AWS WAF takes when a web request doesn't match all conditions in any rule. Valid settings include the following: - ``ALLOW`` : AWS WAF allows requests - ``BLOCK`` : AWS WAF blocks requests - ``COUNT`` : AWS WAF increments a counter of the requests that match all of the conditions in the rule. AWS WAF then continues to inspect the web request based on the remaining rules in the web ACL. You can't specify ``COUNT`` for the default action for a WebACL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                action_property = wafregional_mixins.CfnWebACLPropsMixin.ActionProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d94a259bb9c14d87fc65cc326ff56804245651f995c3093878de54002c152da)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''For actions that are associated with a rule, the action that AWS WAF takes when a web request matches all conditions in a rule.

            For the default action of a web access control list (ACL), the action that AWS WAF takes when a web request doesn't match all conditions in any rule.

            Valid settings include the following:

            - ``ALLOW`` : AWS WAF allows requests
            - ``BLOCK`` : AWS WAF blocks requests
            - ``COUNT`` : AWS WAF increments a counter of the requests that match all of the conditions in the rule. AWS WAF then continues to inspect the web request based on the remaining rules in the web ACL. You can't specify ``COUNT`` for the default action for a WebACL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-action.html#cfn-wafregional-webacl-action-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnWebACLPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "priority": "priority", "rule_id": "ruleId"},
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebACLPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            priority: typing.Optional[jsii.Number] = None,
            rule_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A combination of ``ByteMatchSet`` , ``IPSet`` , and/or ``SqlInjectionMatchSet`` objects that identify the web requests that you want to allow, block, or count.

            For example, you might create a ``Rule`` that includes the following predicates:

            - An ``IPSet`` that causes AWS WAF to search for web requests that originate from the IP address ``192.0.2.44``
            - A ``ByteMatchSet`` that causes AWS WAF to search for web requests for which the value of the ``User-Agent`` header is ``BadBot`` .

            To match the settings in this ``Rule`` , a request must originate from ``192.0.2.44`` AND include a ``User-Agent`` header for which the value is ``BadBot`` .

            :param action: The action that AWS WAF takes when a web request matches all conditions in the rule, such as allow, block, or count the request.
            :param priority: The order in which AWS WAF evaluates the rules in a web ACL. AWS WAF evaluates rules with a lower value before rules with a higher value. The value must be a unique integer. If you have multiple rules in a web ACL, the priority numbers do not need to be consecutive.
            :param rule_id: The ID of an AWS WAF Regional rule to associate with a web ACL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                rule_property = wafregional_mixins.CfnWebACLPropsMixin.RuleProperty(
                    action=wafregional_mixins.CfnWebACLPropsMixin.ActionProperty(
                        type="type"
                    ),
                    priority=123,
                    rule_id="ruleId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57161c309ae178ba398f12d182a8221c7972450451155cc3656b87fa815ca6ad)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if priority is not None:
                self._values["priority"] = priority
            if rule_id is not None:
                self._values["rule_id"] = rule_id

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebACLPropsMixin.ActionProperty"]]:
            '''The action that AWS WAF takes when a web request matches all conditions in the rule, such as allow, block, or count the request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html#cfn-wafregional-webacl-rule-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebACLPropsMixin.ActionProperty"]], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The order in which AWS WAF evaluates the rules in a web ACL.

            AWS WAF evaluates rules with a lower value before rules with a higher value. The value must be a unique integer. If you have multiple rules in a web ACL, the priority numbers do not need to be consecutive.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html#cfn-wafregional-webacl-rule-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rule_id(self) -> typing.Optional[builtins.str]:
            '''The ID of an AWS WAF Regional rule to associate with a web ACL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html#cfn-wafregional-webacl-rule-ruleid
            '''
            result = self._values.get("rule_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnXssMatchSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "xss_match_tuples": "xssMatchTuples"},
)
class CfnXssMatchSetMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        xss_match_tuples: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnXssMatchSetPropsMixin.XssMatchTupleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnXssMatchSetPropsMixin.

        :param name: The name, if any, of the ``XssMatchSet`` .
        :param xss_match_tuples: Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
            
            cfn_xss_match_set_mixin_props = wafregional_mixins.CfnXssMatchSetMixinProps(
                name="name",
                xss_match_tuples=[wafregional_mixins.CfnXssMatchSetPropsMixin.XssMatchTupleProperty(
                    field_to_match=wafregional_mixins.CfnXssMatchSetPropsMixin.FieldToMatchProperty(
                        data="data",
                        type="type"
                    ),
                    text_transformation="textTransformation"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8287cd67fa422b8178f9f29029371bc97a3e19203b5ee5c3e6bdf24f1c93af8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument xss_match_tuples", value=xss_match_tuples, expected_type=type_hints["xss_match_tuples"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if xss_match_tuples is not None:
            self._values["xss_match_tuples"] = xss_match_tuples

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name, if any, of the ``XssMatchSet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html#cfn-wafregional-xssmatchset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def xss_match_tuples(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnXssMatchSetPropsMixin.XssMatchTupleProperty"]]]]:
        '''Specifies the parts of web requests that you want to inspect for cross-site scripting attacks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html#cfn-wafregional-xssmatchset-xssmatchtuples
        '''
        result = self._values.get("xss_match_tuples")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnXssMatchSetPropsMixin.XssMatchTupleProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnXssMatchSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnXssMatchSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnXssMatchSetPropsMixin",
):
    '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

    .. epigraph::

       This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

       *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

    A complex type that contains ``XssMatchTuple`` objects, which specify the parts of web requests that you want AWS WAF to inspect for cross-site scripting attacks and, if you want AWS WAF to inspect a header, the name of the header. If a ``XssMatchSet`` contains more than one ``XssMatchTuple`` object, a request needs to include cross-site scripting attacks in only one of the specified parts of the request to be considered a match.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html
    :cloudformationResource: AWS::WAFRegional::XssMatchSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
        
        cfn_xss_match_set_props_mixin = wafregional_mixins.CfnXssMatchSetPropsMixin(wafregional_mixins.CfnXssMatchSetMixinProps(
            name="name",
            xss_match_tuples=[wafregional_mixins.CfnXssMatchSetPropsMixin.XssMatchTupleProperty(
                field_to_match=wafregional_mixins.CfnXssMatchSetPropsMixin.FieldToMatchProperty(
                    data="data",
                    type="type"
                ),
                text_transformation="textTransformation"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnXssMatchSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::WAFRegional::XssMatchSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c7caa3fe4c902090ec8ff331f6243ba3bb006c77bc4d68998b2544025ce7231)
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
            type_hints = typing.get_type_hints(_typecheckingstub__044d0105850625d3b253b1503d5b6b9c4d0458cd59eafcc7d2fd7e3ab5317e11)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a7071175cf2267f67cbaa5bd01a3a9d115dc63c7b304b51eef8c12edef09baf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnXssMatchSetMixinProps:
        return typing.cast(CfnXssMatchSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnXssMatchSetPropsMixin.FieldToMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"data": "data", "type": "type"},
    )
    class FieldToMatchProperty:
        def __init__(
            self,
            *,
            data: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The part of a web request that you want AWS WAF to inspect, such as a specific header or a query string.

            :param data: When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` . The name of the header is not case sensitive. When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive. If the value of ``Type`` is any other value, omit ``Data`` .
            :param type: The part of the web request that you want AWS WAF to search for a specified string. Parts of a request that you can search include the following: - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` . - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform. - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any. - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` . - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set. - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters. - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-fieldtomatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                field_to_match_property = wafregional_mixins.CfnXssMatchSetPropsMixin.FieldToMatchProperty(
                    data="data",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8652a5e937ad9e2828860209fd581f819739b8de023291d7ec7c8c6515c332d0)
                check_type(argname="argument data", value=data, expected_type=type_hints["data"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data is not None:
                self._values["data"] = data
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def data(self) -> typing.Optional[builtins.str]:
            '''When the value of ``Type`` is ``HEADER`` , enter the name of the header that you want AWS WAF to search, for example, ``User-Agent`` or ``Referer`` .

            The name of the header is not case sensitive.

            When the value of ``Type`` is ``SINGLE_QUERY_ARG`` , enter the name of the parameter that you want AWS WAF to search, for example, ``UserName`` or ``SalesRegion`` . The parameter name is not case sensitive.

            If the value of ``Type`` is any other value, omit ``Data`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-fieldtomatch.html#cfn-wafregional-xssmatchset-fieldtomatch-data
            '''
            result = self._values.get("data")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The part of the web request that you want AWS WAF to search for a specified string.

            Parts of a request that you can search include the following:

            - ``HEADER`` : A specified request header, for example, the value of the ``User-Agent`` or ``Referer`` header. If you choose ``HEADER`` for the type, specify the name of the header in ``Data`` .
            - ``METHOD`` : The HTTP method, which indicates the type of operation that the request is asking the origin to perform.
            - ``QUERY_STRING`` : A query string, which is the part of a URL that appears after a ``?`` character, if any.
            - ``URI`` : The part of a web request that identifies a resource, for example, ``/images/daily-ad.jpg`` .
            - ``BODY`` : The part of a request that contains any additional data that you want to send to your web server as the HTTP request body, such as data from a form. The request body immediately follows the request headers. Note that only the first ``8192`` bytes of the request body are forwarded to AWS WAF for inspection. To allow or block requests based on the length of the body, you can create a size constraint set.
            - ``SINGLE_QUERY_ARG`` : The parameter in the query string that you will inspect, such as *UserName* or *SalesRegion* . The maximum length for ``SINGLE_QUERY_ARG`` is 30 characters.
            - ``ALL_QUERY_ARGS`` : Similar to ``SINGLE_QUERY_ARG`` , but rather than inspecting a single parameter, AWS WAF will inspect all parameters within the query for the value or regex pattern that you specify in ``TargetString`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-fieldtomatch.html#cfn-wafregional-xssmatchset-fieldtomatch-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldToMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wafregional.mixins.CfnXssMatchSetPropsMixin.XssMatchTupleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "field_to_match": "fieldToMatch",
            "text_transformation": "textTransformation",
        },
    )
    class XssMatchTupleProperty:
        def __init__(
            self,
            *,
            field_to_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnXssMatchSetPropsMixin.FieldToMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            text_transformation: typing.Optional[builtins.str] = None,
        ) -> None:
            '''.. epigraph::

   AWS WAF Classic support will end on September 30, 2025.

            .. epigraph::

               This is *AWS WAF Classic* documentation. For more information, see `AWS WAF Classic <https://docs.aws.amazon.com/waf/latest/developerguide/classic-waf-chapter.html>`_ in the developer guide.

               *For the latest version of AWS WAF* , use the AWS WAF V2 API and see the `AWS WAF Developer Guide <https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>`_ . With the latest version, AWS WAF has a single set of endpoints for regional and global use.

            Specifies the part of a web request that you want AWS WAF to inspect for cross-site scripting attacks and, if you want AWS WAF to inspect a header, the name of the header.

            :param field_to_match: The part of a web request that you want AWS WAF to inspect, such as a specified header or a query string.
            :param text_transformation: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF . If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match. You can only specify a single type of TextTransformation. *CMD_LINE* When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations: - Delete the following characters: \\ " ' ^ - Delete spaces before the following characters: / ( - Replace the following characters with a space: , ; - Replace multiple spaces with one space - Convert uppercase letters (A-Z) to lowercase (a-z) *COMPRESS_WHITE_SPACE* Use this option to replace the following characters with a space character (decimal 32): - \\f, formfeed, decimal 12 - \\t, tab, decimal 9 - \\n, newline, decimal 10 - \\r, carriage return, decimal 13 - \\v, vertical tab, decimal 11 - non-breaking space, decimal 160 ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space. *HTML_ENTITY_DECODE* Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations: - Replaces ``(ampersand)quot;`` with ``"`` - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160 - Replaces ``(ampersand)lt;`` with a "less than" symbol - Replaces ``(ampersand)gt;`` with ``>`` - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters *LOWERCASE* Use this option to convert uppercase letters (A-Z) to lowercase (a-z). *URL_DECODE* Use this option to decode a URL-encoded value. *NONE* Specify ``NONE`` if you don't want to perform any text transformations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-xssmatchtuple.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wafregional import mixins as wafregional_mixins
                
                xss_match_tuple_property = wafregional_mixins.CfnXssMatchSetPropsMixin.XssMatchTupleProperty(
                    field_to_match=wafregional_mixins.CfnXssMatchSetPropsMixin.FieldToMatchProperty(
                        data="data",
                        type="type"
                    ),
                    text_transformation="textTransformation"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f17e06d6aa88bfb16382f81bf4b7e45799c311e2c9fc3fdbd2bf95c69209f6e)
                check_type(argname="argument field_to_match", value=field_to_match, expected_type=type_hints["field_to_match"])
                check_type(argname="argument text_transformation", value=text_transformation, expected_type=type_hints["text_transformation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_to_match is not None:
                self._values["field_to_match"] = field_to_match
            if text_transformation is not None:
                self._values["text_transformation"] = text_transformation

        @builtins.property
        def field_to_match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnXssMatchSetPropsMixin.FieldToMatchProperty"]]:
            '''The part of a web request that you want AWS WAF to inspect, such as a specified header or a query string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-xssmatchtuple.html#cfn-wafregional-xssmatchset-xssmatchtuple-fieldtomatch
            '''
            result = self._values.get("field_to_match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnXssMatchSetPropsMixin.FieldToMatchProperty"]], result)

        @builtins.property
        def text_transformation(self) -> typing.Optional[builtins.str]:
            '''Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass AWS WAF .

            If you specify a transformation, AWS WAF performs the transformation on ``FieldToMatch`` before inspecting it for a match.

            You can only specify a single type of TextTransformation.

            *CMD_LINE*

            When you're concerned that attackers are injecting an operating system command line command and using unusual formatting to disguise some or all of the command, use this option to perform the following transformations:

            - Delete the following characters: \\ " ' ^
            - Delete spaces before the following characters: / (
            - Replace the following characters with a space: , ;
            - Replace multiple spaces with one space
            - Convert uppercase letters (A-Z) to lowercase (a-z)

            *COMPRESS_WHITE_SPACE*

            Use this option to replace the following characters with a space character (decimal 32):

            - \\f, formfeed, decimal 12
            - \\t, tab, decimal 9
            - \\n, newline, decimal 10
            - \\r, carriage return, decimal 13
            - \\v, vertical tab, decimal 11
            - non-breaking space, decimal 160

            ``COMPRESS_WHITE_SPACE`` also replaces multiple spaces with one space.

            *HTML_ENTITY_DECODE*

            Use this option to replace HTML-encoded characters with unencoded characters. ``HTML_ENTITY_DECODE`` performs the following operations:

            - Replaces ``(ampersand)quot;`` with ``"``
            - Replaces ``(ampersand)nbsp;`` with a non-breaking space, decimal 160
            - Replaces ``(ampersand)lt;`` with a "less than" symbol
            - Replaces ``(ampersand)gt;`` with ``>``
            - Replaces characters that are represented in hexadecimal format, ``(ampersand)#xhhhh;`` , with the corresponding characters
            - Replaces characters that are represented in decimal format, ``(ampersand)#nnnn;`` , with the corresponding characters

            *LOWERCASE*

            Use this option to convert uppercase letters (A-Z) to lowercase (a-z).

            *URL_DECODE*

            Use this option to decode a URL-encoded value.

            *NONE*

            Specify ``NONE`` if you don't want to perform any text transformations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-xssmatchtuple.html#cfn-wafregional-xssmatchset-xssmatchtuple-texttransformation
            '''
            result = self._values.get("text_transformation")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "XssMatchTupleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnByteMatchSetMixinProps",
    "CfnByteMatchSetPropsMixin",
    "CfnGeoMatchSetMixinProps",
    "CfnGeoMatchSetPropsMixin",
    "CfnIPSetMixinProps",
    "CfnIPSetPropsMixin",
    "CfnRateBasedRuleMixinProps",
    "CfnRateBasedRulePropsMixin",
    "CfnRegexPatternSetMixinProps",
    "CfnRegexPatternSetPropsMixin",
    "CfnRuleMixinProps",
    "CfnRulePropsMixin",
    "CfnSizeConstraintSetMixinProps",
    "CfnSizeConstraintSetPropsMixin",
    "CfnSqlInjectionMatchSetMixinProps",
    "CfnSqlInjectionMatchSetPropsMixin",
    "CfnWebACLAssociationMixinProps",
    "CfnWebACLAssociationPropsMixin",
    "CfnWebACLMixinProps",
    "CfnWebACLPropsMixin",
    "CfnXssMatchSetMixinProps",
    "CfnXssMatchSetPropsMixin",
]

publication.publish()

def _typecheckingstub__581471ecfb00ddc6473cabd3ca04c80da0171ee64e5a6d66821c94ce32802a93(
    *,
    byte_match_tuples: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnByteMatchSetPropsMixin.ByteMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6dd74a90f738ad4966b74c29c29a94933d64f93f530b8e58d394edc1c92eb7f(
    props: typing.Union[CfnByteMatchSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b054f3024c71efbc4b3e126c6e047b9cecc6fdfe5a3c2e27273d29a5954ecdea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e376061449c65d82efcf012105a21d5b9677b883a20e59e3b28ea4af842fb65(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d963847d6f8e762ea73c263ae2c27cb5f237189b04174ad982847a83a7821f35(
    *,
    field_to_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnByteMatchSetPropsMixin.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    positional_constraint: typing.Optional[builtins.str] = None,
    target_string: typing.Optional[builtins.str] = None,
    target_string_base64: typing.Optional[builtins.str] = None,
    text_transformation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90914177f8d117a2cf0912e37528bc485d16f60eb89654bfaf18d503eace7f7c(
    *,
    data: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f73015d4764c4880f1f4a749c4de52bb927a9ac5aff242667c06eae89857f25(
    *,
    geo_match_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGeoMatchSetPropsMixin.GeoMatchConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9fd5124be3b97ed644fa8319b7a7d65a655901c6f1570aaa8f683b0b8d12ab(
    props: typing.Union[CfnGeoMatchSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea28a21c5293ccf70b4d9f5d63689703357095254a2e42066028c62da79b6dd4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b96da30d83bd7a00c3a94a3fb6ccf4f9d9ea007105fd55f6d4e1ad4fb69e68(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fe3364659887874256b61571ab8f3b2cdae805ba224a0b6c76739a2413c8f3(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babd7cfbb69f0b653a1e24b5ac9a3648e2bcff937cac0224336e31e246e4f194(
    *,
    ip_set_descriptors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIPSetPropsMixin.IPSetDescriptorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a0927fb39a9ae7dc0b39075b446a9022aa337d1afc544c320e0446e489da59(
    props: typing.Union[CfnIPSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35c7f81a544b49e360908db2d0f7147e664fd63434a7cc3fe70450788a2d231(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92786ca018c6a19e7dedfbbff9e2e9fd20bdfb41e3604f1abc54a2df1228d73d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2275bc60a00ae0a66d32fac0f50b919d2a727aa2e439a974707a3d9dca245f(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85db7f38535a8c95ba5d3ddd72b82868720edc98a1cdd349837247154cd4abca(
    *,
    match_predicates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRateBasedRulePropsMixin.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rate_key: typing.Optional[builtins.str] = None,
    rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__184f6611c1e592feebb954d826b04473ca86e0aa063906d39bf161688547046c(
    props: typing.Union[CfnRateBasedRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a54332626b6c6d4ed1ab5580ae8bdcfb0c8efb77b67ca53d35f7c60f8e2386(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f42748979182ec36d6b760ea98dbc5c13ffe9fb7457e995e380c4b46478d12(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148707adfce5a96d55db9455f9545e29a2ae4d3b28aebecdede1fb612a7214af(
    *,
    data_id: typing.Optional[builtins.str] = None,
    negated: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1970cc3cddd4130e60d3bec941a12dc196ae64dac8cd269ae5f165a7881841bf(
    *,
    name: typing.Optional[builtins.str] = None,
    regex_pattern_strings: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8219df53ccacfc3e3ee964955901eda2e6626248cca340baa7e0531d7987942d(
    props: typing.Union[CfnRegexPatternSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1125c95537792d331feb8ab24e34df7646ea9e864251706f306604a0239c853b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f642691e2641ebdddfba2635336ffcbe5f824dd1da44a27087e4813b06ec401c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0cfd0ef69882f962de27979ba8e34d6cf4577a583cd1e2ffc76ae11c97022a(
    *,
    metric_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    predicates: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.PredicateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b22d929b80ef8fb9fb2a92a21ccb1249a24c96c715783a12036bd2ee68d15b(
    props: typing.Union[CfnRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29600b91d56c8ead7c704e1cab82041c31cd8572d9f2044ea44ff3a0affd489d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36f38b8cd5a2242d62c3d9472c20b65b502f31a19981fcaaa62bd7d8055eb48(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47392c5cb06519699ebd0ff40176035920f8afb40e23f048929c44ea1efa9aa7(
    *,
    data_id: typing.Optional[builtins.str] = None,
    negated: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c44329f6354e4b699bf1a016d654ffc03a708fcab0a728214de9d5ca35bacc2(
    *,
    name: typing.Optional[builtins.str] = None,
    size_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSizeConstraintSetPropsMixin.SizeConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070770dd93457e0d5c726bf76eccc7645bf18ccbeb09e0af2ea8e26c4af2f1ec(
    props: typing.Union[CfnSizeConstraintSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da557ffcf09708cfcc8161955d4da1b1e53b052b046c467171f80bf9e292c422(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd2ae92efe810326fc9436dea3ee63789bce1631213045a6ed4c89b5e7c7bc4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5effb2ddf07e3e14cbaa4ab92c82d5608c24f13bcc278dc6117f81de39ea2957(
    *,
    data: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638eda145071ae0eaff85c46c958625fad6cf9db070d7aee0ee2f8e5aa5b09a0(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    field_to_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSizeConstraintSetPropsMixin.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    size: typing.Optional[jsii.Number] = None,
    text_transformation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccdacc71c655d8c4c6e61e00edb3de3fab3f1bee3105b20a33eff5c7a101474(
    *,
    name: typing.Optional[builtins.str] = None,
    sql_injection_match_tuples: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSqlInjectionMatchSetPropsMixin.SqlInjectionMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab6e2ff37fd5854cdca1edbca1ec590f2eb8c1ca2784acba24c8e4a414604c6(
    props: typing.Union[CfnSqlInjectionMatchSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2c1842242fa0488400263a578b0804054c3734a7e25a923947c46b73f53ead(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdac36f2b9d540005a8ebd43bd6f1c34cf19187300d621325c84d48811585ea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47a639a2145147294034aa5b29770c07b7badb17387bad69ef166dda9c27d20(
    *,
    data: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77044b71f7e48a2d3dfc817d6adcaa27cd5d15bd06c9bf6ce53b81f982b3437(
    *,
    field_to_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSqlInjectionMatchSetPropsMixin.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    text_transformation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff6c23cf07cadd7ef7a6488d0b43874c7576003b9b465347b3099bd57b1d56e(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__734e3ece604640e48574e580c8a7184602fd48beccb8feb7992569ac080540bf(
    props: typing.Union[CfnWebACLAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffa6bf667cca66447fea504089af7a0feacfd0887ab6678261e4b78212a6bcf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c62ecd7b5c206fb13cb76369c4b66ed1b2e7db0fe661f1574bfab641380c31(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b1aaa9309afc15b64947fa701066c679ac69681b3da83d8f3a3e0695fc0053(
    *,
    default_action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebACLPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebACLPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8847394a1350ffd1a77aacf08a6c5357cc9134025e3d2c604ef7222f1631aed(
    props: typing.Union[CfnWebACLMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0deafe468468c337c9eb0970caac6de5c2888f34a00c3831c4bc0ca22501a4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25984fd39de7ad1eb8f2215a94a81246453797a3067c963cb0a26a2270dcb2fb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d94a259bb9c14d87fc65cc326ff56804245651f995c3093878de54002c152da(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57161c309ae178ba398f12d182a8221c7972450451155cc3656b87fa815ca6ad(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebACLPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    rule_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8287cd67fa422b8178f9f29029371bc97a3e19203b5ee5c3e6bdf24f1c93af8(
    *,
    name: typing.Optional[builtins.str] = None,
    xss_match_tuples: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnXssMatchSetPropsMixin.XssMatchTupleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c7caa3fe4c902090ec8ff331f6243ba3bb006c77bc4d68998b2544025ce7231(
    props: typing.Union[CfnXssMatchSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__044d0105850625d3b253b1503d5b6b9c4d0458cd59eafcc7d2fd7e3ab5317e11(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a7071175cf2267f67cbaa5bd01a3a9d115dc63c7b304b51eef8c12edef09baf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8652a5e937ad9e2828860209fd581f819739b8de023291d7ec7c8c6515c332d0(
    *,
    data: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f17e06d6aa88bfb16382f81bf4b7e45799c311e2c9fc3fdbd2bf95c69209f6e(
    *,
    field_to_match: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnXssMatchSetPropsMixin.FieldToMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    text_transformation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
