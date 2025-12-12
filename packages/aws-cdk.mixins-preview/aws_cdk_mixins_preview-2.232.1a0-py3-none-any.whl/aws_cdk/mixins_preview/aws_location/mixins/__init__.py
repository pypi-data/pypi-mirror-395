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
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnAPIKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "expire_time": "expireTime",
        "force_delete": "forceDelete",
        "force_update": "forceUpdate",
        "key_name": "keyName",
        "no_expiry": "noExpiry",
        "restrictions": "restrictions",
        "tags": "tags",
    },
)
class CfnAPIKeyMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        expire_time: typing.Optional[builtins.str] = None,
        force_delete: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        force_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        key_name: typing.Optional[builtins.str] = None,
        no_expiry: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        restrictions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAPIKeyPropsMixin.ApiKeyRestrictionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAPIKeyPropsMixin.

        :param description: Updates the description for the API key resource.
        :param expire_time: The optional timestamp for when the API key resource will expire in `ISO 8601 format <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ .
        :param force_delete: ForceDelete bypasses an API key's expiry conditions and deletes the key. Set the parameter ``true`` to delete the key or to ``false`` to not preemptively delete the API key. Valid values: ``true`` , or ``false`` . .. epigraph:: This action is irreversible. Only use ForceDelete if you are certain the key is no longer in use.
        :param force_update: The boolean flag to be included for updating ``ExpireTime`` or Restrictions details. Must be set to ``true`` to update an API key resource that has been used in the past 7 days. ``False`` if force update is not preferred.
        :param key_name: A custom name for the API key resource. Requirements: - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique API key name. - No spaces allowed. For example, ``ExampleAPIKey`` .
        :param no_expiry: Whether the API key should expire. Set to ``true`` to set the API key to have no expiration time.
        :param restrictions: The API key restrictions for the API key resource.
        :param tags: Applies one or more tags to the map resource. A tag is a key-value pair that helps manage, identify, search, and filter your resources by labelling them.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
            
            cfn_aPIKey_mixin_props = location_mixins.CfnAPIKeyMixinProps(
                description="description",
                expire_time="expireTime",
                force_delete=False,
                force_update=False,
                key_name="keyName",
                no_expiry=False,
                restrictions=location_mixins.CfnAPIKeyPropsMixin.ApiKeyRestrictionsProperty(
                    allow_actions=["allowActions"],
                    allow_android_apps=[location_mixins.CfnAPIKeyPropsMixin.AndroidAppProperty(
                        certificate_fingerprint="certificateFingerprint",
                        package="package"
                    )],
                    allow_apple_apps=[location_mixins.CfnAPIKeyPropsMixin.AppleAppProperty(
                        bundle_id="bundleId"
                    )],
                    allow_referers=["allowReferers"],
                    allow_resources=["allowResources"]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__563eea72533e36e4d9d450971cce2742a4466b49d5e35e025936022b9566d750)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expire_time", value=expire_time, expected_type=type_hints["expire_time"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument force_update", value=force_update, expected_type=type_hints["force_update"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument no_expiry", value=no_expiry, expected_type=type_hints["no_expiry"])
            check_type(argname="argument restrictions", value=restrictions, expected_type=type_hints["restrictions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if expire_time is not None:
            self._values["expire_time"] = expire_time
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if force_update is not None:
            self._values["force_update"] = force_update
        if key_name is not None:
            self._values["key_name"] = key_name
        if no_expiry is not None:
            self._values["no_expiry"] = no_expiry
        if restrictions is not None:
            self._values["restrictions"] = restrictions
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Updates the description for the API key resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html#cfn-location-apikey-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expire_time(self) -> typing.Optional[builtins.str]:
        '''The optional timestamp for when the API key resource will expire in `ISO 8601 format <https://docs.aws.amazon.com/https://www.iso.org/iso-8601-date-and-time-format.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html#cfn-location-apikey-expiretime
        '''
        result = self._values.get("expire_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''ForceDelete bypasses an API key's expiry conditions and deletes the key.

        Set the parameter ``true`` to delete the key or to ``false`` to not preemptively delete the API key.

        Valid values: ``true`` , or ``false`` .
        .. epigraph::

           This action is irreversible. Only use ForceDelete if you are certain the key is no longer in use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html#cfn-location-apikey-forcedelete
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def force_update(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The boolean flag to be included for updating ``ExpireTime`` or Restrictions details.

        Must be set to ``true`` to update an API key resource that has been used in the past 7 days. ``False`` if force update is not preferred.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html#cfn-location-apikey-forceupdate
        '''
        result = self._values.get("force_update")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''A custom name for the API key resource.

        Requirements:

        - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique API key name.
        - No spaces allowed. For example, ``ExampleAPIKey`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html#cfn-location-apikey-keyname
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_expiry(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether the API key should expire.

        Set to ``true`` to set the API key to have no expiration time.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html#cfn-location-apikey-noexpiry
        '''
        result = self._values.get("no_expiry")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def restrictions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAPIKeyPropsMixin.ApiKeyRestrictionsProperty"]]:
        '''The API key restrictions for the API key resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html#cfn-location-apikey-restrictions
        '''
        result = self._values.get("restrictions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAPIKeyPropsMixin.ApiKeyRestrictionsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Applies one or more tags to the map resource.

        A tag is a key-value pair that helps manage, identify, search, and filter your resources by labelling them.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html#cfn-location-apikey-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAPIKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAPIKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnAPIKeyPropsMixin",
):
    '''The API key resource in your AWS account, which lets you grant actions for Amazon Location resources to the API key bearer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-apikey.html
    :cloudformationResource: AWS::Location::APIKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
        
        cfn_aPIKey_props_mixin = location_mixins.CfnAPIKeyPropsMixin(location_mixins.CfnAPIKeyMixinProps(
            description="description",
            expire_time="expireTime",
            force_delete=False,
            force_update=False,
            key_name="keyName",
            no_expiry=False,
            restrictions=location_mixins.CfnAPIKeyPropsMixin.ApiKeyRestrictionsProperty(
                allow_actions=["allowActions"],
                allow_android_apps=[location_mixins.CfnAPIKeyPropsMixin.AndroidAppProperty(
                    certificate_fingerprint="certificateFingerprint",
                    package="package"
                )],
                allow_apple_apps=[location_mixins.CfnAPIKeyPropsMixin.AppleAppProperty(
                    bundle_id="bundleId"
                )],
                allow_referers=["allowReferers"],
                allow_resources=["allowResources"]
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
        props: typing.Union[CfnAPIKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Location::APIKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e8542c1418c8ccf3a88b0461ce92bae7ae63aa91d4bd68c219637dfb099a60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbf109327bb9c5bb3867e67df081049f88a0ee9558504e1da4e8f992cbb86a1b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc4cb71c55771cd6107865b2a2d3fae63f2869ac32f9e6feac731849316bb6d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAPIKeyMixinProps:
        return typing.cast(CfnAPIKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnAPIKeyPropsMixin.AndroidAppProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_fingerprint": "certificateFingerprint",
            "package": "package",
        },
    )
    class AndroidAppProperty:
        def __init__(
            self,
            *,
            certificate_fingerprint: typing.Optional[builtins.str] = None,
            package: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param certificate_fingerprint: 
            :param package: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-androidapp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
                
                android_app_property = location_mixins.CfnAPIKeyPropsMixin.AndroidAppProperty(
                    certificate_fingerprint="certificateFingerprint",
                    package="package"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__041dd202e515a6e26a8d479ecbab48aff3b044073ffa3c599402d3cb2faa6d78)
                check_type(argname="argument certificate_fingerprint", value=certificate_fingerprint, expected_type=type_hints["certificate_fingerprint"])
                check_type(argname="argument package", value=package, expected_type=type_hints["package"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_fingerprint is not None:
                self._values["certificate_fingerprint"] = certificate_fingerprint
            if package is not None:
                self._values["package"] = package

        @builtins.property
        def certificate_fingerprint(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-androidapp.html#cfn-location-apikey-androidapp-certificatefingerprint
            '''
            result = self._values.get("certificate_fingerprint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def package(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-androidapp.html#cfn-location-apikey-androidapp-package
            '''
            result = self._values.get("package")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AndroidAppProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnAPIKeyPropsMixin.ApiKeyRestrictionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_actions": "allowActions",
            "allow_android_apps": "allowAndroidApps",
            "allow_apple_apps": "allowAppleApps",
            "allow_referers": "allowReferers",
            "allow_resources": "allowResources",
        },
    )
    class ApiKeyRestrictionsProperty:
        def __init__(
            self,
            *,
            allow_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_android_apps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAPIKeyPropsMixin.AndroidAppProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            allow_apple_apps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAPIKeyPropsMixin.AppleAppProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            allow_referers: typing.Optional[typing.Sequence[builtins.str]] = None,
            allow_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''API Restrictions on the allowed actions, resources, and referers for an API key resource.

            :param allow_actions: A list of allowed actions that an API key resource grants permissions to perform. You must have at least one action for each type of resource. For example, if you have a place resource, you must include at least one place action. The following are valid values for the actions. - *Map actions* - ``geo:GetMap*`` - Allows all actions needed for map rendering. - *Enhanced Maps actions* - ``geo-maps:GetTile`` - Allows getting map tiles for rendering. - ``geo-maps:GetStaticMap`` - Allows getting static map images. - *Place actions* - ``geo:SearchPlaceIndexForText`` - Allows finding geo coordinates of a known place. - ``geo:SearchPlaceIndexForPosition`` - Allows getting nearest address to geo coordinates. - ``geo:SearchPlaceIndexForSuggestions`` - Allows suggestions based on an incomplete or misspelled query. - ``geo:GetPlace`` - Allows getting details of a place. - *Enhanced Places actions* - ``geo-places:Autcomplete`` - Allows auto-completion of search text. - ``geo-places:Geocode`` - Allows finding geo coordinates of a known place. - ``geo-places:GetPlace`` - Allows getting details of a place. - ``geo-places:ReverseGeocode`` - Allows getting nearest address to geo coordinates. - ``geo-places:SearchNearby`` - Allows category based places search around geo coordinates. - ``geo-places:SearchText`` - Allows place or address search based on free-form text. - ``geo-places:Suggest`` - Allows suggestions based on an incomplete or misspelled query. - *Route actions* - ``geo:CalculateRoute`` - Allows point to point routing. - ``geo:CalculateRouteMatrix`` - Allows matrix routing. - *Enhanced Routes actions* - ``geo-routes:CalculateIsolines`` - Allows isoline calculation. - ``geo-routes:CalculateRoutes`` - Allows point to point routing. - ``geo-routes:CalculateRouteMatrix`` - Allows matrix routing. - ``geo-routes:OptimizeWaypoints`` - Allows computing the best sequence of waypoints. - ``geo-routes:SnapToRoads`` - Allows snapping GPS points to a likely route. .. epigraph:: You must use these strings exactly. For example, to provide access to map rendering, the only valid action is ``geo:GetMap*`` as an input to the list. ``["geo:GetMap*"]`` is valid but ``["geo:GetTile"]`` is not. Similarly, you cannot use ``["geo:SearchPlaceIndexFor*"]`` - you must list each of the Place actions separately.
            :param allow_android_apps: 
            :param allow_apple_apps: 
            :param allow_referers: An optional list of allowed HTTP referers for which requests must originate from. Requests using this API key from other domains will not be allowed. Requirements: - Contain only alphanumeric characters (A–Z, a–z, 0–9) or any symbols in this list ``$\\-._+!*``(),;/?:@=&` - May contain a percent (%) if followed by 2 hexadecimal digits (A-F, a-f, 0-9); this is used for URL encoding purposes. - May contain wildcard characters question mark (?) and asterisk (*). Question mark (?) will replace any single character (including hexadecimal digits). Asterisk (*) will replace any multiple characters (including multiple hexadecimal digits). - No spaces allowed. For example, ``https://example.com`` .
            :param allow_resources: A list of allowed resource ARNs that a API key bearer can perform actions on. - The ARN must be the correct ARN for a map, place, or route ARN. You may include wildcards in the resource-id to match multiple resources of the same type. - The resources must be in the same ``partition`` , ``region`` , and ``account-id`` as the key that is being created. - Other than wildcards, you must include the full ARN, including the ``arn`` , ``partition`` , ``service`` , ``region`` , ``account-id`` and ``resource-id`` delimited by colons (:). - No spaces allowed, even with wildcards. For example, ``arn:aws:geo:region: *account-id* :map/ExampleMap*`` . For more information about ARN format, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-apikeyrestrictions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
                
                api_key_restrictions_property = location_mixins.CfnAPIKeyPropsMixin.ApiKeyRestrictionsProperty(
                    allow_actions=["allowActions"],
                    allow_android_apps=[location_mixins.CfnAPIKeyPropsMixin.AndroidAppProperty(
                        certificate_fingerprint="certificateFingerprint",
                        package="package"
                    )],
                    allow_apple_apps=[location_mixins.CfnAPIKeyPropsMixin.AppleAppProperty(
                        bundle_id="bundleId"
                    )],
                    allow_referers=["allowReferers"],
                    allow_resources=["allowResources"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58cf573c98331de9ba274ce0713ea6abab56aa71d9df9eee6b545e7bcaee4f6f)
                check_type(argname="argument allow_actions", value=allow_actions, expected_type=type_hints["allow_actions"])
                check_type(argname="argument allow_android_apps", value=allow_android_apps, expected_type=type_hints["allow_android_apps"])
                check_type(argname="argument allow_apple_apps", value=allow_apple_apps, expected_type=type_hints["allow_apple_apps"])
                check_type(argname="argument allow_referers", value=allow_referers, expected_type=type_hints["allow_referers"])
                check_type(argname="argument allow_resources", value=allow_resources, expected_type=type_hints["allow_resources"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_actions is not None:
                self._values["allow_actions"] = allow_actions
            if allow_android_apps is not None:
                self._values["allow_android_apps"] = allow_android_apps
            if allow_apple_apps is not None:
                self._values["allow_apple_apps"] = allow_apple_apps
            if allow_referers is not None:
                self._values["allow_referers"] = allow_referers
            if allow_resources is not None:
                self._values["allow_resources"] = allow_resources

        @builtins.property
        def allow_actions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of allowed actions that an API key resource grants permissions to perform.

            You must have at least one action for each type of resource. For example, if you have a place resource, you must include at least one place action.

            The following are valid values for the actions.

            - *Map actions*
            - ``geo:GetMap*`` - Allows all actions needed for map rendering.
            - *Enhanced Maps actions*
            - ``geo-maps:GetTile`` - Allows getting map tiles for rendering.
            - ``geo-maps:GetStaticMap`` - Allows getting static map images.
            - *Place actions*
            - ``geo:SearchPlaceIndexForText`` - Allows finding geo coordinates of a known place.
            - ``geo:SearchPlaceIndexForPosition`` - Allows getting nearest address to geo coordinates.
            - ``geo:SearchPlaceIndexForSuggestions`` - Allows suggestions based on an incomplete or misspelled query.
            - ``geo:GetPlace`` - Allows getting details of a place.
            - *Enhanced Places actions*
            - ``geo-places:Autcomplete`` - Allows auto-completion of search text.
            - ``geo-places:Geocode`` - Allows finding geo coordinates of a known place.
            - ``geo-places:GetPlace`` - Allows getting details of a place.
            - ``geo-places:ReverseGeocode`` - Allows getting nearest address to geo coordinates.
            - ``geo-places:SearchNearby`` - Allows category based places search around geo coordinates.
            - ``geo-places:SearchText`` - Allows place or address search based on free-form text.
            - ``geo-places:Suggest`` - Allows suggestions based on an incomplete or misspelled query.
            - *Route actions*
            - ``geo:CalculateRoute`` - Allows point to point routing.
            - ``geo:CalculateRouteMatrix`` - Allows matrix routing.
            - *Enhanced Routes actions*
            - ``geo-routes:CalculateIsolines`` - Allows isoline calculation.
            - ``geo-routes:CalculateRoutes`` - Allows point to point routing.
            - ``geo-routes:CalculateRouteMatrix`` - Allows matrix routing.
            - ``geo-routes:OptimizeWaypoints`` - Allows computing the best sequence of waypoints.
            - ``geo-routes:SnapToRoads`` - Allows snapping GPS points to a likely route.

            .. epigraph::

               You must use these strings exactly. For example, to provide access to map rendering, the only valid action is ``geo:GetMap*`` as an input to the list. ``["geo:GetMap*"]`` is valid but ``["geo:GetTile"]`` is not. Similarly, you cannot use ``["geo:SearchPlaceIndexFor*"]`` - you must list each of the Place actions separately.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-apikeyrestrictions.html#cfn-location-apikey-apikeyrestrictions-allowactions
            '''
            result = self._values.get("allow_actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_android_apps(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAPIKeyPropsMixin.AndroidAppProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-apikeyrestrictions.html#cfn-location-apikey-apikeyrestrictions-allowandroidapps
            '''
            result = self._values.get("allow_android_apps")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAPIKeyPropsMixin.AndroidAppProperty"]]]], result)

        @builtins.property
        def allow_apple_apps(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAPIKeyPropsMixin.AppleAppProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-apikeyrestrictions.html#cfn-location-apikey-apikeyrestrictions-allowappleapps
            '''
            result = self._values.get("allow_apple_apps")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAPIKeyPropsMixin.AppleAppProperty"]]]], result)

        @builtins.property
        def allow_referers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An optional list of allowed HTTP referers for which requests must originate from.

            Requests using this API key from other domains will not be allowed.

            Requirements:

            - Contain only alphanumeric characters (A–Z, a–z, 0–9) or any symbols in this list ``$\\-._+!*``(),;/?:@=&`
            - May contain a percent (%) if followed by 2 hexadecimal digits (A-F, a-f, 0-9); this is used for URL encoding purposes.
            - May contain wildcard characters question mark (?) and asterisk (*).

            Question mark (?) will replace any single character (including hexadecimal digits).

            Asterisk (*) will replace any multiple characters (including multiple hexadecimal digits).

            - No spaces allowed. For example, ``https://example.com`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-apikeyrestrictions.html#cfn-location-apikey-apikeyrestrictions-allowreferers
            '''
            result = self._values.get("allow_referers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def allow_resources(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of allowed resource ARNs that a API key bearer can perform actions on.

            - The ARN must be the correct ARN for a map, place, or route ARN. You may include wildcards in the resource-id to match multiple resources of the same type.
            - The resources must be in the same ``partition`` , ``region`` , and ``account-id`` as the key that is being created.
            - Other than wildcards, you must include the full ARN, including the ``arn`` , ``partition`` , ``service`` , ``region`` , ``account-id`` and ``resource-id`` delimited by colons (:).
            - No spaces allowed, even with wildcards. For example, ``arn:aws:geo:region: *account-id* :map/ExampleMap*`` .

            For more information about ARN format, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-apikeyrestrictions.html#cfn-location-apikey-apikeyrestrictions-allowresources
            '''
            result = self._values.get("allow_resources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiKeyRestrictionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnAPIKeyPropsMixin.AppleAppProperty",
        jsii_struct_bases=[],
        name_mapping={"bundle_id": "bundleId"},
    )
    class AppleAppProperty:
        def __init__(self, *, bundle_id: typing.Optional[builtins.str] = None) -> None:
            '''
            :param bundle_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-appleapp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
                
                apple_app_property = location_mixins.CfnAPIKeyPropsMixin.AppleAppProperty(
                    bundle_id="bundleId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__478fb388a604a5574b2dfcc57986d734985b1adff222a979a204ccc521a62f16)
                check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bundle_id is not None:
                self._values["bundle_id"] = bundle_id

        @builtins.property
        def bundle_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-apikey-appleapp.html#cfn-location-apikey-appleapp-bundleid
            '''
            result = self._values.get("bundle_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppleAppProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnGeofenceCollectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "collection_name": "collectionName",
        "description": "description",
        "kms_key_id": "kmsKeyId",
        "pricing_plan": "pricingPlan",
        "pricing_plan_data_source": "pricingPlanDataSource",
        "tags": "tags",
    },
)
class CfnGeofenceCollectionMixinProps:
    def __init__(
        self,
        *,
        collection_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        pricing_plan_data_source: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGeofenceCollectionPropsMixin.

        :param collection_name: A custom name for the geofence collection. Requirements: - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique geofence collection name. - No spaces allowed. For example, ``ExampleGeofenceCollection`` .
        :param description: An optional description for the geofence collection.
        :param kms_key_id: A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.
        :param pricing_plan: 
        :param pricing_plan_data_source: (deprecated) This shape is deprecated since 2022-02-01: Deprecated. No longer allowed.
        :param tags: Applies one or more tags to the geofence collection. A tag is a key-value pair helps manage, identify, search, and filter your resources by labelling them. Format: ``"key" : "value"`` Restrictions: - Maximum 50 tags per resource - Each resource tag must be unique with a maximum of one value. - Maximum key length: 128 Unicode characters in UTF-8 - Maximum value length: 256 Unicode characters in UTF-8 - Can use alphanumeric characters (A–Z, a–z, 0–9), and the following characters: + - = . _ : /

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
            
            cfn_geofence_collection_mixin_props = location_mixins.CfnGeofenceCollectionMixinProps(
                collection_name="collectionName",
                description="description",
                kms_key_id="kmsKeyId",
                pricing_plan="pricingPlan",
                pricing_plan_data_source="pricingPlanDataSource",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb5dd792a037fde1d3ecff525672f0b8f7e6cb07d14044ee17aa6c7974ebfd4)
            check_type(argname="argument collection_name", value=collection_name, expected_type=type_hints["collection_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
            check_type(argname="argument pricing_plan_data_source", value=pricing_plan_data_source, expected_type=type_hints["pricing_plan_data_source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collection_name is not None:
            self._values["collection_name"] = collection_name
        if description is not None:
            self._values["description"] = description
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan
        if pricing_plan_data_source is not None:
            self._values["pricing_plan_data_source"] = pricing_plan_data_source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def collection_name(self) -> typing.Optional[builtins.str]:
        '''A custom name for the geofence collection.

        Requirements:

        - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique geofence collection name.
        - No spaces allowed. For example, ``ExampleGeofenceCollection`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-collectionname
        '''
        result = self._values.get("collection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the geofence collection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-pricingplan
        :stability: deprecated
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan_data_source(self) -> typing.Optional[builtins.str]:
        '''(deprecated) This shape is deprecated since 2022-02-01: Deprecated.

        No longer allowed.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-pricingplandatasource
        :stability: deprecated
        '''
        result = self._values.get("pricing_plan_data_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Applies one or more tags to the geofence collection.

        A tag is a key-value pair helps manage, identify, search, and filter your resources by labelling them.

        Format: ``"key" : "value"``

        Restrictions:

        - Maximum 50 tags per resource
        - Each resource tag must be unique with a maximum of one value.
        - Maximum key length: 128 Unicode characters in UTF-8
        - Maximum value length: 256 Unicode characters in UTF-8
        - Can use alphanumeric characters (A–Z, a–z, 0–9), and the following characters: + - = . _ : /

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html#cfn-location-geofencecollection-tags
        ::

        .

        - Cannot use "aws:" as a prefix for a key.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGeofenceCollectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGeofenceCollectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnGeofenceCollectionPropsMixin",
):
    '''The ``AWS::Location::GeofenceCollection`` resource specifies the ability to detect and act when a tracked device enters or exits a defined geographical boundary known as a geofence.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-geofencecollection.html
    :cloudformationResource: AWS::Location::GeofenceCollection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
        
        cfn_geofence_collection_props_mixin = location_mixins.CfnGeofenceCollectionPropsMixin(location_mixins.CfnGeofenceCollectionMixinProps(
            collection_name="collectionName",
            description="description",
            kms_key_id="kmsKeyId",
            pricing_plan="pricingPlan",
            pricing_plan_data_source="pricingPlanDataSource",
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
        props: typing.Union[CfnGeofenceCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Location::GeofenceCollection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff390b4930573cad180846acc0496d8cf800d2321aaa647891ef0d48c467af3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__126de7eceb45726258a6f8cc3e15ff44342accf76394eab4c8afd314e77f2769)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8736caadd990f8362ca803c853181df3d6a832cd6c1730745db33f3256f6c486)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGeofenceCollectionMixinProps:
        return typing.cast(CfnGeofenceCollectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnMapMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "description": "description",
        "map_name": "mapName",
        "pricing_plan": "pricingPlan",
        "tags": "tags",
    },
)
class CfnMapMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMapPropsMixin.MapConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        map_name: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMapPropsMixin.

        :param configuration: Specifies the ``MapConfiguration`` , including the map style, for the map resource that you create. The map style defines the look of maps and the data provider for your map resource.
        :param description: An optional description for the map resource.
        :param map_name: The name for the map resource. Requirements: - Must contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique map resource name. - No spaces allowed. For example, ``ExampleMap`` .
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``
        :param tags: Applies one or more tags to the map resource. A tag is a key-value pair helps manage, identify, search, and filter your resources by labelling them. Format: ``"key" : "value"`` Restrictions: - Maximum 50 tags per resource - Each resource tag must be unique with a maximum of one value. - Maximum key length: 128 Unicode characters in UTF-8 - Maximum value length: 256 Unicode characters in UTF-8 - Can use alphanumeric characters (A–Z, a–z, 0–9), and the following characters: + - = . _ : /

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
            
            cfn_map_mixin_props = location_mixins.CfnMapMixinProps(
                configuration=location_mixins.CfnMapPropsMixin.MapConfigurationProperty(
                    custom_layers=["customLayers"],
                    political_view="politicalView",
                    style="style"
                ),
                description="description",
                map_name="mapName",
                pricing_plan="pricingPlan",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23bb2c8730b57b43491eb33dd31382b4a8147d814402b538b8aa7a4e6b11826d)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument map_name", value=map_name, expected_type=type_hints["map_name"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if map_name is not None:
            self._values["map_name"] = map_name
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMapPropsMixin.MapConfigurationProperty"]]:
        '''Specifies the ``MapConfiguration`` , including the map style, for the map resource that you create.

        The map style defines the look of maps and the data provider for your map resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMapPropsMixin.MapConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the map resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def map_name(self) -> typing.Optional[builtins.str]:
        '''The name for the map resource.

        Requirements:

        - Must contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique map resource name.
        - No spaces allowed. For example, ``ExampleMap`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-mapname
        '''
        result = self._values.get("map_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-pricingplan
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Applies one or more tags to the map resource.

        A tag is a key-value pair helps manage, identify, search, and filter your resources by labelling them.

        Format: ``"key" : "value"``

        Restrictions:

        - Maximum 50 tags per resource
        - Each resource tag must be unique with a maximum of one value.
        - Maximum key length: 128 Unicode characters in UTF-8
        - Maximum value length: 256 Unicode characters in UTF-8
        - Can use alphanumeric characters (A–Z, a–z, 0–9), and the following characters: + - = . _ : /

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html#cfn-location-map-tags
        ::

        .

        - Cannot use "aws:" as a prefix for a key.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMapMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMapPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnMapPropsMixin",
):
    '''The ``AWS::Location::Map`` resource specifies a map resource in your AWS account, which provides map tiles of different styles sourced from global location data providers.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-map.html
    :cloudformationResource: AWS::Location::Map
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
        
        cfn_map_props_mixin = location_mixins.CfnMapPropsMixin(location_mixins.CfnMapMixinProps(
            configuration=location_mixins.CfnMapPropsMixin.MapConfigurationProperty(
                custom_layers=["customLayers"],
                political_view="politicalView",
                style="style"
            ),
            description="description",
            map_name="mapName",
            pricing_plan="pricingPlan",
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
        props: typing.Union[CfnMapMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Location::Map``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c1642021d4c8871999a3aa207e15df126a51aff73032850457c73e978a3777f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c11f4d809a7c7aefd3852fd019813ff5d68e2c12ad94dd2c74047fa3888f5a1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbe6d40e1f663451162647deb80d9674277b8de7290fa4389f62e8f779feb63)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMapMixinProps:
        return typing.cast(CfnMapMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnMapPropsMixin.MapConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_layers": "customLayers",
            "political_view": "politicalView",
            "style": "style",
        },
    )
    class MapConfigurationProperty:
        def __init__(
            self,
            *,
            custom_layers: typing.Optional[typing.Sequence[builtins.str]] = None,
            political_view: typing.Optional[builtins.str] = None,
            style: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the map tile style selected from an available provider.

            :param custom_layers: Specifies the custom layers for the style. Leave unset to not enable any custom layer, or, for styles that support custom layers, you can enable layer(s), such as the ``POI`` layer for the VectorEsriNavigation style. .. epigraph:: Currenlty only ``VectorEsriNavigation`` supports CustomLayers. For more information, see `Custom Layers <https://docs.aws.amazon.com//location/latest/developerguide/map-concepts.html#map-custom-layers>`_ .
            :param political_view: Specifies the map political view selected from an available data provider.
            :param style: Specifies the map style selected from an available data provider. Valid `Esri map styles <https://docs.aws.amazon.com/location/previous/developerguide/esri.html>`_ : - ``VectorEsriDarkGrayCanvas`` – The Esri Dark Gray Canvas map style. A vector basemap with a dark gray, neutral background with minimal colors, labels, and features that's designed to draw attention to your thematic content. - ``RasterEsriImagery`` – The Esri Imagery map style. A raster basemap that provides one meter or better satellite and aerial imagery in many parts of the world and lower resolution satellite imagery worldwide. - ``VectorEsriLightGrayCanvas`` – The Esri Light Gray Canvas map style, which provides a detailed vector basemap with a light gray, neutral background style with minimal colors, labels, and features that's designed to draw attention to your thematic content. - ``VectorEsriTopographic`` – The Esri Light map style, which provides a detailed vector basemap with a classic Esri map style. - ``VectorEsriStreets`` – The Esri Street Map style, which provides a detailed vector basemap for the world symbolized with a classic Esri street map style. The vector tile layer is similar in content and style to the World Street Map raster map. - ``VectorEsriNavigation`` – The Esri Navigation map style, which provides a detailed basemap for the world symbolized with a custom navigation map style that's designed for use during the day in mobile devices. Valid `HERE Technologies map styles <https://docs.aws.amazon.com/location/previous/developerguide/HERE.html>`_ : - ``VectorHereContrast`` – The HERE Contrast (Berlin) map style is a high contrast detailed base map of the world that blends 3D and 2D rendering. .. epigraph:: The ``VectorHereContrast`` style has been renamed from ``VectorHereBerlin`` . ``VectorHereBerlin`` has been deprecated, but will continue to work in applications that use it. - ``VectorHereExplore`` – A default HERE map style containing a neutral, global map and its features including roads, buildings, landmarks, and water features. It also now includes a fully designed map of Japan. - ``VectorHereExploreTruck`` – A global map containing truck restrictions and attributes (e.g. width / height / HAZMAT) symbolized with highlighted segments and icons on top of HERE Explore to support use cases within transport and logistics. - ``RasterHereExploreSatellite`` – A global map containing high resolution satellite imagery. - ``HybridHereExploreSatellite`` – A global map displaying the road network, street names, and city labels over satellite imagery. This style will automatically retrieve both raster and vector tiles, and your charges will be based on total tiles retrieved. .. epigraph:: Hybrid styles use both vector and raster tiles when rendering the map that you see. This means that more tiles are retrieved than when using either vector or raster tiles alone. Your charges will include all tiles retrieved. Valid `GrabMaps map styles <https://docs.aws.amazon.com/location/previous/developerguide/grab.html>`_ : - ``VectorGrabStandardLight`` – The Grab Standard Light map style provides a basemap with detailed land use coloring, area names, roads, landmarks, and points of interest covering Southeast Asia. - ``VectorGrabStandardDark`` – The Grab Standard Dark map style provides a dark variation of the standard basemap covering Southeast Asia. .. epigraph:: Grab provides maps only for countries in Southeast Asia, and is only available in the Asia Pacific (Singapore) Region ( ``ap-southeast-1`` ). For more information, see `GrabMaps countries and area covered <https://docs.aws.amazon.com/location/previous/developerguide/grab.html#grab-coverage-area>`_ . Valid `Open Data map styles <https://docs.aws.amazon.com/location/previous/developerguide/open-data.html>`_ : - ``VectorOpenDataStandardLight`` – The Open Data Standard Light map style provides a detailed basemap for the world suitable for website and mobile application use. The map includes highways major roads, minor roads, railways, water features, cities, parks, landmarks, building footprints, and administrative boundaries. - ``VectorOpenDataStandardDark`` – Open Data Standard Dark is a dark-themed map style that provides a detailed basemap for the world suitable for website and mobile application use. The map includes highways major roads, minor roads, railways, water features, cities, parks, landmarks, building footprints, and administrative boundaries. - ``VectorOpenDataVisualizationLight`` – The Open Data Visualization Light map style is a light-themed style with muted colors and fewer features that aids in understanding overlaid data. - ``VectorOpenDataVisualizationDark`` – The Open Data Visualization Dark map style is a dark-themed style with muted colors and fewer features that aids in understanding overlaid data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-map-mapconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
                
                map_configuration_property = location_mixins.CfnMapPropsMixin.MapConfigurationProperty(
                    custom_layers=["customLayers"],
                    political_view="politicalView",
                    style="style"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c22deef2ecb9753275c07f5d07673cacea6b36647ce516ebd17d71ff146cdb0a)
                check_type(argname="argument custom_layers", value=custom_layers, expected_type=type_hints["custom_layers"])
                check_type(argname="argument political_view", value=political_view, expected_type=type_hints["political_view"])
                check_type(argname="argument style", value=style, expected_type=type_hints["style"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_layers is not None:
                self._values["custom_layers"] = custom_layers
            if political_view is not None:
                self._values["political_view"] = political_view
            if style is not None:
                self._values["style"] = style

        @builtins.property
        def custom_layers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the custom layers for the style.

            Leave unset to not enable any custom layer, or, for styles that support custom layers, you can enable layer(s), such as the ``POI`` layer for the VectorEsriNavigation style.
            .. epigraph::

               Currenlty only ``VectorEsriNavigation`` supports CustomLayers. For more information, see `Custom Layers <https://docs.aws.amazon.com//location/latest/developerguide/map-concepts.html#map-custom-layers>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-map-mapconfiguration.html#cfn-location-map-mapconfiguration-customlayers
            '''
            result = self._values.get("custom_layers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def political_view(self) -> typing.Optional[builtins.str]:
            '''Specifies the map political view selected from an available data provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-map-mapconfiguration.html#cfn-location-map-mapconfiguration-politicalview
            '''
            result = self._values.get("political_view")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def style(self) -> typing.Optional[builtins.str]:
            '''Specifies the map style selected from an available data provider.

            Valid `Esri map styles <https://docs.aws.amazon.com/location/previous/developerguide/esri.html>`_ :

            - ``VectorEsriDarkGrayCanvas`` – The Esri Dark Gray Canvas map style. A vector basemap with a dark gray, neutral background with minimal colors, labels, and features that's designed to draw attention to your thematic content.
            - ``RasterEsriImagery`` – The Esri Imagery map style. A raster basemap that provides one meter or better satellite and aerial imagery in many parts of the world and lower resolution satellite imagery worldwide.
            - ``VectorEsriLightGrayCanvas`` – The Esri Light Gray Canvas map style, which provides a detailed vector basemap with a light gray, neutral background style with minimal colors, labels, and features that's designed to draw attention to your thematic content.
            - ``VectorEsriTopographic`` – The Esri Light map style, which provides a detailed vector basemap with a classic Esri map style.
            - ``VectorEsriStreets`` – The Esri Street Map style, which provides a detailed vector basemap for the world symbolized with a classic Esri street map style. The vector tile layer is similar in content and style to the World Street Map raster map.
            - ``VectorEsriNavigation`` – The Esri Navigation map style, which provides a detailed basemap for the world symbolized with a custom navigation map style that's designed for use during the day in mobile devices.

            Valid `HERE Technologies map styles <https://docs.aws.amazon.com/location/previous/developerguide/HERE.html>`_ :

            - ``VectorHereContrast`` – The HERE Contrast (Berlin) map style is a high contrast detailed base map of the world that blends 3D and 2D rendering.

            .. epigraph::

               The ``VectorHereContrast`` style has been renamed from ``VectorHereBerlin`` . ``VectorHereBerlin`` has been deprecated, but will continue to work in applications that use it.

            - ``VectorHereExplore`` – A default HERE map style containing a neutral, global map and its features including roads, buildings, landmarks, and water features. It also now includes a fully designed map of Japan.
            - ``VectorHereExploreTruck`` – A global map containing truck restrictions and attributes (e.g. width / height / HAZMAT) symbolized with highlighted segments and icons on top of HERE Explore to support use cases within transport and logistics.
            - ``RasterHereExploreSatellite`` – A global map containing high resolution satellite imagery.
            - ``HybridHereExploreSatellite`` – A global map displaying the road network, street names, and city labels over satellite imagery. This style will automatically retrieve both raster and vector tiles, and your charges will be based on total tiles retrieved.

            .. epigraph::

               Hybrid styles use both vector and raster tiles when rendering the map that you see. This means that more tiles are retrieved than when using either vector or raster tiles alone. Your charges will include all tiles retrieved.

            Valid `GrabMaps map styles <https://docs.aws.amazon.com/location/previous/developerguide/grab.html>`_ :

            - ``VectorGrabStandardLight`` – The Grab Standard Light map style provides a basemap with detailed land use coloring, area names, roads, landmarks, and points of interest covering Southeast Asia.
            - ``VectorGrabStandardDark`` – The Grab Standard Dark map style provides a dark variation of the standard basemap covering Southeast Asia.

            .. epigraph::

               Grab provides maps only for countries in Southeast Asia, and is only available in the Asia Pacific (Singapore) Region ( ``ap-southeast-1`` ). For more information, see `GrabMaps countries and area covered <https://docs.aws.amazon.com/location/previous/developerguide/grab.html#grab-coverage-area>`_ .

            Valid `Open Data map styles <https://docs.aws.amazon.com/location/previous/developerguide/open-data.html>`_ :

            - ``VectorOpenDataStandardLight`` – The Open Data Standard Light map style provides a detailed basemap for the world suitable for website and mobile application use. The map includes highways major roads, minor roads, railways, water features, cities, parks, landmarks, building footprints, and administrative boundaries.
            - ``VectorOpenDataStandardDark`` – Open Data Standard Dark is a dark-themed map style that provides a detailed basemap for the world suitable for website and mobile application use. The map includes highways major roads, minor roads, railways, water features, cities, parks, landmarks, building footprints, and administrative boundaries.
            - ``VectorOpenDataVisualizationLight`` – The Open Data Visualization Light map style is a light-themed style with muted colors and fewer features that aids in understanding overlaid data.
            - ``VectorOpenDataVisualizationDark`` – The Open Data Visualization Dark map style is a dark-themed style with muted colors and fewer features that aids in understanding overlaid data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-map-mapconfiguration.html#cfn-location-map-mapconfiguration-style
            '''
            result = self._values.get("style")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MapConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnPlaceIndexMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_source": "dataSource",
        "data_source_configuration": "dataSourceConfiguration",
        "description": "description",
        "index_name": "indexName",
        "pricing_plan": "pricingPlan",
        "tags": "tags",
    },
)
class CfnPlaceIndexMixinProps:
    def __init__(
        self,
        *,
        data_source: typing.Optional[builtins.str] = None,
        data_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlaceIndexPropsMixin.DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        index_name: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPlaceIndexPropsMixin.

        :param data_source: Specifies the geospatial data provider for the new place index. .. epigraph:: This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error. Valid values include: - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/previous/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on geocoding coverage <https://docs.aws.amazon.com/https://developers.arcgis.com/rest/geocode/api-reference/geocode-coverage.htm>`_ . - ``Grab`` – Grab provides place index functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/previous/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/previous/developerguide/grab.html#grab-coverage-area>`_ . - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/previous/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE details on goecoding coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/geocoder/dev_guide/topics/coverage-geocoder.html>`_ . .. epigraph:: If you specify HERE Technologies ( ``Here`` ) as the data provider, you may not `store results <https://docs.aws.amazon.com//location-places/latest/APIReference/API_DataSourceConfiguration.html>`_ for locations in Japan. For more information, see the `AWS service terms <https://docs.aws.amazon.com/service-terms/>`_ for Amazon Location Service. For additional information , see `Data providers <https://docs.aws.amazon.com/location/previous/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service developer guide* .
        :param data_source_configuration: Specifies the data storage option requesting Places.
        :param description: The optional description for the place index resource.
        :param index_name: The name of the place index resource. Requirements: - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_). - Must be a unique place index resource name. - No spaces allowed. For example, ``ExamplePlaceIndex`` .
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
            
            cfn_place_index_mixin_props = location_mixins.CfnPlaceIndexMixinProps(
                data_source="dataSource",
                data_source_configuration=location_mixins.CfnPlaceIndexPropsMixin.DataSourceConfigurationProperty(
                    intended_use="intendedUse"
                ),
                description="description",
                index_name="indexName",
                pricing_plan="pricingPlan",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522080d3c60480841661cc7e6354c6a046c67827c1c3c24ea02bb01b372fa83e)
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument data_source_configuration", value=data_source_configuration, expected_type=type_hints["data_source_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_source is not None:
            self._values["data_source"] = data_source
        if data_source_configuration is not None:
            self._values["data_source_configuration"] = data_source_configuration
        if description is not None:
            self._values["description"] = description
        if index_name is not None:
            self._values["index_name"] = index_name
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_source(self) -> typing.Optional[builtins.str]:
        '''Specifies the geospatial data provider for the new place index.

        .. epigraph::

           This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error.

        Valid values include:

        - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/previous/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on geocoding coverage <https://docs.aws.amazon.com/https://developers.arcgis.com/rest/geocode/api-reference/geocode-coverage.htm>`_ .
        - ``Grab`` – Grab provides place index functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/previous/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/previous/developerguide/grab.html#grab-coverage-area>`_ .
        - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/previous/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE details on goecoding coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/geocoder/dev_guide/topics/coverage-geocoder.html>`_ .

        .. epigraph::

           If you specify HERE Technologies ( ``Here`` ) as the data provider, you may not `store results <https://docs.aws.amazon.com//location-places/latest/APIReference/API_DataSourceConfiguration.html>`_ for locations in Japan. For more information, see the `AWS service terms <https://docs.aws.amazon.com/service-terms/>`_ for Amazon Location Service.

        For additional information , see `Data providers <https://docs.aws.amazon.com/location/previous/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service developer guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-datasource
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaceIndexPropsMixin.DataSourceConfigurationProperty"]]:
        '''Specifies the data storage option requesting Places.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-datasourceconfiguration
        '''
        result = self._values.get("data_source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlaceIndexPropsMixin.DataSourceConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The optional description for the place index resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_name(self) -> typing.Optional[builtins.str]:
        '''The name of the place index resource.

        Requirements:

        - Contain only alphanumeric characters (A–Z, a–z, 0–9), hyphens (-), periods (.), and underscores (_).
        - Must be a unique place index resource name.
        - No spaces allowed. For example, ``ExamplePlaceIndex`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-indexname
        '''
        result = self._values.get("index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-pricingplan
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html#cfn-location-placeindex-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlaceIndexMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPlaceIndexPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnPlaceIndexPropsMixin",
):
    '''Specifies a place index resource in your AWS account.

    Use a place index resource to geocode addresses and other text queries by using the ``SearchPlaceIndexForText`` operation, and reverse geocode coordinates by using the ``SearchPlaceIndexForPosition`` operation, and enable autosuggestions by using the ``SearchPlaceIndexForSuggestions`` operation.
    .. epigraph::

       If your application is tracking or routing assets you use in your business, such as delivery vehicles or employees, you must not use Esri as your geolocation provider. See section 82 of the `AWS service terms <https://docs.aws.amazon.com/service-terms>`_ for more details.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-placeindex.html
    :cloudformationResource: AWS::Location::PlaceIndex
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
        
        cfn_place_index_props_mixin = location_mixins.CfnPlaceIndexPropsMixin(location_mixins.CfnPlaceIndexMixinProps(
            data_source="dataSource",
            data_source_configuration=location_mixins.CfnPlaceIndexPropsMixin.DataSourceConfigurationProperty(
                intended_use="intendedUse"
            ),
            description="description",
            index_name="indexName",
            pricing_plan="pricingPlan",
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
        props: typing.Union[CfnPlaceIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Location::PlaceIndex``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241d744e50c85cea0b61f26b9b9025a5d79d7e828e7db35b3c19a44dad04ea35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d38b8b806c0a1e1f5fdabf9cb6c71e2e6d8821be427e9f73d6df20a9667cde3a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00ed7d34266035ae227fc24c565b4d3b55a8a50cca3e0280e28e98063fbdcd9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPlaceIndexMixinProps:
        return typing.cast(CfnPlaceIndexMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnPlaceIndexPropsMixin.DataSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"intended_use": "intendedUse"},
    )
    class DataSourceConfigurationProperty:
        def __init__(
            self,
            *,
            intended_use: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the data storage option requesting Places.

            :param intended_use: Specifies how the results of an operation will be stored by the caller. Valid values include: - ``SingleUse`` specifies that the results won't be stored. - ``Storage`` specifies that the result can be cached or stored in a database. Default value: ``SingleUse``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-placeindex-datasourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
                
                data_source_configuration_property = location_mixins.CfnPlaceIndexPropsMixin.DataSourceConfigurationProperty(
                    intended_use="intendedUse"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b10f88e6abbb475201c2a956d8a4366504c1d7b3d3071a004c5a09a936c90344)
                check_type(argname="argument intended_use", value=intended_use, expected_type=type_hints["intended_use"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if intended_use is not None:
                self._values["intended_use"] = intended_use

        @builtins.property
        def intended_use(self) -> typing.Optional[builtins.str]:
            '''Specifies how the results of an operation will be stored by the caller.

            Valid values include:

            - ``SingleUse`` specifies that the results won't be stored.
            - ``Storage`` specifies that the result can be cached or stored in a database.

            Default value: ``SingleUse``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-location-placeindex-datasourceconfiguration.html#cfn-location-placeindex-datasourceconfiguration-intendeduse
            '''
            result = self._values.get("intended_use")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnRouteCalculatorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "calculator_name": "calculatorName",
        "data_source": "dataSource",
        "description": "description",
        "pricing_plan": "pricingPlan",
        "tags": "tags",
    },
)
class CfnRouteCalculatorMixinProps:
    def __init__(
        self,
        *,
        calculator_name: typing.Optional[builtins.str] = None,
        data_source: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRouteCalculatorPropsMixin.

        :param calculator_name: The name of the route calculator resource. Requirements: - Can use alphanumeric characters (A–Z, a–z, 0–9) , hyphens (-), periods (.), and underscores (_). - Must be a unique Route calculator resource name. - No spaces allowed. For example, ``ExampleRouteCalculator`` .
        :param data_source: Specifies the data provider of traffic and road network data. .. epigraph:: This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error. Valid values include: - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/previous/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on street networks and traffic coverage <https://docs.aws.amazon.com/https://doc.arcgis.com/en/arcgis-online/reference/network-coverage.htm>`_ . Route calculators that use Esri as a data source only calculate routes that are shorter than 400 km. - ``Grab`` – Grab provides routing functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/previous/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/previous/developerguide/grab.html#grab-coverage-area>`_ . - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/previous/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE car routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/car-routing.html>`_ and `HERE truck routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/truck-routing.html>`_ . For additional information , see `Data providers <https://docs.aws.amazon.com/location/previous/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .
        :param description: The optional description for the route calculator resource.
        :param pricing_plan: No longer used. If included, the only allowed value is ``RequestBasedUsage`` . *Allowed Values* : ``RequestBasedUsage``
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
            
            cfn_route_calculator_mixin_props = location_mixins.CfnRouteCalculatorMixinProps(
                calculator_name="calculatorName",
                data_source="dataSource",
                description="description",
                pricing_plan="pricingPlan",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3da25d608eb03573bc26b77127a996d3930b10a1b7f81195e7ec72e59388c10)
            check_type(argname="argument calculator_name", value=calculator_name, expected_type=type_hints["calculator_name"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if calculator_name is not None:
            self._values["calculator_name"] = calculator_name
        if data_source is not None:
            self._values["data_source"] = data_source
        if description is not None:
            self._values["description"] = description
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def calculator_name(self) -> typing.Optional[builtins.str]:
        '''The name of the route calculator resource.

        Requirements:

        - Can use alphanumeric characters (A–Z, a–z, 0–9) , hyphens (-), periods (.), and underscores (_).
        - Must be a unique Route calculator resource name.
        - No spaces allowed. For example, ``ExampleRouteCalculator`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-calculatorname
        '''
        result = self._values.get("calculator_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_source(self) -> typing.Optional[builtins.str]:
        '''Specifies the data provider of traffic and road network data.

        .. epigraph::

           This field is case-sensitive. Enter the valid values as shown. For example, entering ``HERE`` returns an error.

        Valid values include:

        - ``Esri`` – For additional information about `Esri <https://docs.aws.amazon.com/location/previous/developerguide/esri.html>`_ 's coverage in your region of interest, see `Esri details on street networks and traffic coverage <https://docs.aws.amazon.com/https://doc.arcgis.com/en/arcgis-online/reference/network-coverage.htm>`_ .

        Route calculators that use Esri as a data source only calculate routes that are shorter than 400 km.

        - ``Grab`` – Grab provides routing functionality for Southeast Asia. For additional information about `GrabMaps <https://docs.aws.amazon.com/location/previous/developerguide/grab.html>`_ ' coverage, see `GrabMaps countries and areas covered <https://docs.aws.amazon.com/location/previous/developerguide/grab.html#grab-coverage-area>`_ .
        - ``Here`` – For additional information about `HERE Technologies <https://docs.aws.amazon.com/location/previous/developerguide/HERE.html>`_ ' coverage in your region of interest, see `HERE car routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/car-routing.html>`_ and `HERE truck routing coverage <https://docs.aws.amazon.com/https://developer.here.com/documentation/routing-api/dev_guide/topics/coverage/truck-routing.html>`_ .

        For additional information , see `Data providers <https://docs.aws.amazon.com/location/previous/developerguide/what-is-data-provider.html>`_ on the *Amazon Location Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-datasource
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The optional description for the route calculator resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''No longer used. If included, the only allowed value is ``RequestBasedUsage`` .

        *Allowed Values* : ``RequestBasedUsage``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-pricingplan
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html#cfn-location-routecalculator-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRouteCalculatorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRouteCalculatorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnRouteCalculatorPropsMixin",
):
    '''Specifies a route calculator resource in your AWS account.

    You can send requests to a route calculator resource to estimate travel time, distance, and get directions. A route calculator sources traffic and road network data from your chosen data provider.
    .. epigraph::

       If your application is tracking or routing assets you use in your business, such as delivery vehicles or employees, you must not use Esri as your geolocation provider. See section 82 of the `AWS service terms <https://docs.aws.amazon.com/service-terms>`_ for more details.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-routecalculator.html
    :cloudformationResource: AWS::Location::RouteCalculator
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
        
        cfn_route_calculator_props_mixin = location_mixins.CfnRouteCalculatorPropsMixin(location_mixins.CfnRouteCalculatorMixinProps(
            calculator_name="calculatorName",
            data_source="dataSource",
            description="description",
            pricing_plan="pricingPlan",
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
        props: typing.Union[CfnRouteCalculatorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Location::RouteCalculator``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5146f411a6ed3c91a3f2c4064a22e8b9c950ce2a16a02102f8eccf9c3d28293)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cc4c7f36d452041572605f5efca219339a91e820dcc6417612416d3b3efd9a4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f038d510a241f5665a475e1ef1aec1a81d06b3ae27ed86fe2e32924d7763484)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRouteCalculatorMixinProps:
        return typing.cast(CfnRouteCalculatorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnTrackerConsumerMixinProps",
    jsii_struct_bases=[],
    name_mapping={"consumer_arn": "consumerArn", "tracker_name": "trackerName"},
)
class CfnTrackerConsumerMixinProps:
    def __init__(
        self,
        *,
        consumer_arn: typing.Optional[builtins.str] = None,
        tracker_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTrackerConsumerPropsMixin.

        :param consumer_arn: The Amazon Resource Name (ARN) for the geofence collection to be associated to tracker resource. Used when you need to specify a resource across all AWS . - Format example: ``arn:aws:geo:region:account-id:geofence-collection/ExampleGeofenceCollectionConsumer``
        :param tracker_name: The name for the tracker resource. Requirements: - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_). - Must be a unique tracker resource name. - No spaces allowed. For example, ``ExampleTracker`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
            
            cfn_tracker_consumer_mixin_props = location_mixins.CfnTrackerConsumerMixinProps(
                consumer_arn="consumerArn",
                tracker_name="trackerName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb9ff3cef3e36741b2cde4387fc2e63637ee26042299a175f08f66c194cd9c6)
            check_type(argname="argument consumer_arn", value=consumer_arn, expected_type=type_hints["consumer_arn"])
            check_type(argname="argument tracker_name", value=tracker_name, expected_type=type_hints["tracker_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumer_arn is not None:
            self._values["consumer_arn"] = consumer_arn
        if tracker_name is not None:
            self._values["tracker_name"] = tracker_name

    @builtins.property
    def consumer_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the geofence collection to be associated to tracker resource.

        Used when you need to specify a resource across all AWS .

        - Format example: ``arn:aws:geo:region:account-id:geofence-collection/ExampleGeofenceCollectionConsumer``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html#cfn-location-trackerconsumer-consumerarn
        '''
        result = self._values.get("consumer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tracker_name(self) -> typing.Optional[builtins.str]:
        '''The name for the tracker resource.

        Requirements:

        - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_).
        - Must be a unique tracker resource name.
        - No spaces allowed. For example, ``ExampleTracker`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html#cfn-location-trackerconsumer-trackername
        '''
        result = self._values.get("tracker_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrackerConsumerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrackerConsumerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnTrackerConsumerPropsMixin",
):
    '''The ``AWS::Location::TrackerConsumer`` resource specifies an association between a geofence collection and a tracker resource.

    The geofence collection is referred to as the *consumer* of the tracker. This allows the tracker resource to communicate location data to the linked geofence collection.
    .. epigraph::

       Currently not supported — Cross-account configurations, such as creating associations between a tracker resource in one account and a geofence collection in another account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-trackerconsumer.html
    :cloudformationResource: AWS::Location::TrackerConsumer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
        
        cfn_tracker_consumer_props_mixin = location_mixins.CfnTrackerConsumerPropsMixin(location_mixins.CfnTrackerConsumerMixinProps(
            consumer_arn="consumerArn",
            tracker_name="trackerName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTrackerConsumerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Location::TrackerConsumer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__210dd32b254c5a51e79ab674b357bda6c02181a9a791fff7e0b16bf1ef51ef05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a775008e27efd90b43eee6ce0240f3f664d9d8459efbd920059b73d2229263d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf1ac131f4c3c04f6fe07acef5bae5c97cc5bf90a50de8b8ccb93356608e0c4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrackerConsumerMixinProps:
        return typing.cast(CfnTrackerConsumerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnTrackerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "event_bridge_enabled": "eventBridgeEnabled",
        "kms_key_enable_geospatial_queries": "kmsKeyEnableGeospatialQueries",
        "kms_key_id": "kmsKeyId",
        "position_filtering": "positionFiltering",
        "pricing_plan": "pricingPlan",
        "pricing_plan_data_source": "pricingPlanDataSource",
        "tags": "tags",
        "tracker_name": "trackerName",
    },
)
class CfnTrackerMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_bridge_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        kms_key_enable_geospatial_queries: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        position_filtering: typing.Optional[builtins.str] = None,
        pricing_plan: typing.Optional[builtins.str] = None,
        pricing_plan_data_source: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tracker_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTrackerPropsMixin.

        :param description: An optional description for the tracker resource.
        :param event_bridge_enabled: 
        :param kms_key_enable_geospatial_queries: 
        :param kms_key_id: A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.
        :param position_filtering: Specifies the position filtering for the tracker resource. Valid values: - ``TimeBased`` - Location updates are evaluated against linked geofence collections, but not every location update is stored. If your update frequency is more often than 30 seconds, only one update per 30 seconds is stored for each unique device ID. - ``DistanceBased`` - If the device has moved less than 30 m (98.4 ft), location updates are ignored. Location updates within this area are neither evaluated against linked geofence collections, nor stored. This helps control costs by reducing the number of geofence evaluations and historical device positions to paginate through. Distance-based filtering can also reduce the effects of GPS noise when displaying device trajectories on a map. - ``AccuracyBased`` - If the device has moved less than the measured accuracy, location updates are ignored. For example, if two consecutive updates from a device have a horizontal accuracy of 5 m and 10 m, the second update is ignored if the device has moved less than 15 m. Ignored location updates are neither evaluated against linked geofence collections, nor stored. This can reduce the effects of GPS noise when displaying device trajectories on a map, and can help control your costs by reducing the number of geofence evaluations. This field is optional. If not specified, the default value is ``TimeBased`` .
        :param pricing_plan: 
        :param pricing_plan_data_source: (deprecated) This shape is deprecated since 2022-02-01: Deprecated. No longer allowed.
        :param tags: An array of key-value pairs to apply to this resource.
        :param tracker_name: The name for the tracker resource. Requirements: - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_). - Must be a unique tracker resource name. - No spaces allowed. For example, ``ExampleTracker`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
            
            cfn_tracker_mixin_props = location_mixins.CfnTrackerMixinProps(
                description="description",
                event_bridge_enabled=False,
                kms_key_enable_geospatial_queries=False,
                kms_key_id="kmsKeyId",
                position_filtering="positionFiltering",
                pricing_plan="pricingPlan",
                pricing_plan_data_source="pricingPlanDataSource",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tracker_name="trackerName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb8a1bb8f7dbe12e2cdabc96bc9c69dd616df5cca7769ba81f65be433913637)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_bridge_enabled", value=event_bridge_enabled, expected_type=type_hints["event_bridge_enabled"])
            check_type(argname="argument kms_key_enable_geospatial_queries", value=kms_key_enable_geospatial_queries, expected_type=type_hints["kms_key_enable_geospatial_queries"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument position_filtering", value=position_filtering, expected_type=type_hints["position_filtering"])
            check_type(argname="argument pricing_plan", value=pricing_plan, expected_type=type_hints["pricing_plan"])
            check_type(argname="argument pricing_plan_data_source", value=pricing_plan_data_source, expected_type=type_hints["pricing_plan_data_source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tracker_name", value=tracker_name, expected_type=type_hints["tracker_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_bridge_enabled is not None:
            self._values["event_bridge_enabled"] = event_bridge_enabled
        if kms_key_enable_geospatial_queries is not None:
            self._values["kms_key_enable_geospatial_queries"] = kms_key_enable_geospatial_queries
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if position_filtering is not None:
            self._values["position_filtering"] = position_filtering
        if pricing_plan is not None:
            self._values["pricing_plan"] = pricing_plan
        if pricing_plan_data_source is not None:
            self._values["pricing_plan_data_source"] = pricing_plan_data_source
        if tags is not None:
            self._values["tags"] = tags
        if tracker_name is not None:
            self._values["tracker_name"] = tracker_name

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for the tracker resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_bridge_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-eventbridgeenabled
        '''
        result = self._values.get("event_bridge_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def kms_key_enable_geospatial_queries(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-kmskeyenablegeospatialqueries
        '''
        result = self._values.get("kms_key_enable_geospatial_queries")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''A key identifier for an `AWS KMS customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html>`_ . Enter a key ID, key ARN, alias name, or alias ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def position_filtering(self) -> typing.Optional[builtins.str]:
        '''Specifies the position filtering for the tracker resource.

        Valid values:

        - ``TimeBased`` - Location updates are evaluated against linked geofence collections, but not every location update is stored. If your update frequency is more often than 30 seconds, only one update per 30 seconds is stored for each unique device ID.
        - ``DistanceBased`` - If the device has moved less than 30 m (98.4 ft), location updates are ignored. Location updates within this area are neither evaluated against linked geofence collections, nor stored. This helps control costs by reducing the number of geofence evaluations and historical device positions to paginate through. Distance-based filtering can also reduce the effects of GPS noise when displaying device trajectories on a map.
        - ``AccuracyBased`` - If the device has moved less than the measured accuracy, location updates are ignored. For example, if two consecutive updates from a device have a horizontal accuracy of 5 m and 10 m, the second update is ignored if the device has moved less than 15 m. Ignored location updates are neither evaluated against linked geofence collections, nor stored. This can reduce the effects of GPS noise when displaying device trajectories on a map, and can help control your costs by reducing the number of geofence evaluations.

        This field is optional. If not specified, the default value is ``TimeBased`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-positionfiltering
        '''
        result = self._values.get("position_filtering")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan(self) -> typing.Optional[builtins.str]:
        '''
        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-pricingplan
        :stability: deprecated
        '''
        result = self._values.get("pricing_plan")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pricing_plan_data_source(self) -> typing.Optional[builtins.str]:
        '''(deprecated) This shape is deprecated since 2022-02-01: Deprecated.

        No longer allowed.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-pricingplandatasource
        :stability: deprecated
        '''
        result = self._values.get("pricing_plan_data_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tracker_name(self) -> typing.Optional[builtins.str]:
        '''The name for the tracker resource.

        Requirements:

        - Contain only alphanumeric characters (A-Z, a-z, 0-9) , hyphens (-), periods (.), and underscores (_).
        - Must be a unique tracker resource name.
        - No spaces allowed. For example, ``ExampleTracker`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html#cfn-location-tracker-trackername
        '''
        result = self._values.get("tracker_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrackerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrackerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_location.mixins.CfnTrackerPropsMixin",
):
    '''Specifies a tracker resource in your AWS account , which lets you receive current and historical location of devices.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-location-tracker.html
    :cloudformationResource: AWS::Location::Tracker
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_location import mixins as location_mixins
        
        cfn_tracker_props_mixin = location_mixins.CfnTrackerPropsMixin(location_mixins.CfnTrackerMixinProps(
            description="description",
            event_bridge_enabled=False,
            kms_key_enable_geospatial_queries=False,
            kms_key_id="kmsKeyId",
            position_filtering="positionFiltering",
            pricing_plan="pricingPlan",
            pricing_plan_data_source="pricingPlanDataSource",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tracker_name="trackerName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTrackerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Location::Tracker``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f1ace89ac5e08711cc5b877bafe86721690e8798a482ee4eaa37b3b1178c69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d41aced6a6b3ce9ffeb78df5d8cad32c0e546b4245d751011752bba5f288e86e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bb65bd4abb916ab747dac18c1068ee796ce1ece419c0a258ae9d78f063a599)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrackerMixinProps:
        return typing.cast(CfnTrackerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAPIKeyMixinProps",
    "CfnAPIKeyPropsMixin",
    "CfnGeofenceCollectionMixinProps",
    "CfnGeofenceCollectionPropsMixin",
    "CfnMapMixinProps",
    "CfnMapPropsMixin",
    "CfnPlaceIndexMixinProps",
    "CfnPlaceIndexPropsMixin",
    "CfnRouteCalculatorMixinProps",
    "CfnRouteCalculatorPropsMixin",
    "CfnTrackerConsumerMixinProps",
    "CfnTrackerConsumerPropsMixin",
    "CfnTrackerMixinProps",
    "CfnTrackerPropsMixin",
]

publication.publish()

def _typecheckingstub__563eea72533e36e4d9d450971cce2742a4466b49d5e35e025936022b9566d750(
    *,
    description: typing.Optional[builtins.str] = None,
    expire_time: typing.Optional[builtins.str] = None,
    force_delete: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    force_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_name: typing.Optional[builtins.str] = None,
    no_expiry: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    restrictions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAPIKeyPropsMixin.ApiKeyRestrictionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e8542c1418c8ccf3a88b0461ce92bae7ae63aa91d4bd68c219637dfb099a60(
    props: typing.Union[CfnAPIKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf109327bb9c5bb3867e67df081049f88a0ee9558504e1da4e8f992cbb86a1b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc4cb71c55771cd6107865b2a2d3fae63f2869ac32f9e6feac731849316bb6d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041dd202e515a6e26a8d479ecbab48aff3b044073ffa3c599402d3cb2faa6d78(
    *,
    certificate_fingerprint: typing.Optional[builtins.str] = None,
    package: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58cf573c98331de9ba274ce0713ea6abab56aa71d9df9eee6b545e7bcaee4f6f(
    *,
    allow_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_android_apps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAPIKeyPropsMixin.AndroidAppProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    allow_apple_apps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAPIKeyPropsMixin.AppleAppProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    allow_referers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478fb388a604a5574b2dfcc57986d734985b1adff222a979a204ccc521a62f16(
    *,
    bundle_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb5dd792a037fde1d3ecff525672f0b8f7e6cb07d14044ee17aa6c7974ebfd4(
    *,
    collection_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    pricing_plan_data_source: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff390b4930573cad180846acc0496d8cf800d2321aaa647891ef0d48c467af3(
    props: typing.Union[CfnGeofenceCollectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126de7eceb45726258a6f8cc3e15ff44342accf76394eab4c8afd314e77f2769(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8736caadd990f8362ca803c853181df3d6a832cd6c1730745db33f3256f6c486(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23bb2c8730b57b43491eb33dd31382b4a8147d814402b538b8aa7a4e6b11826d(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMapPropsMixin.MapConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    map_name: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1642021d4c8871999a3aa207e15df126a51aff73032850457c73e978a3777f(
    props: typing.Union[CfnMapMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c11f4d809a7c7aefd3852fd019813ff5d68e2c12ad94dd2c74047fa3888f5a1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbe6d40e1f663451162647deb80d9674277b8de7290fa4389f62e8f779feb63(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22deef2ecb9753275c07f5d07673cacea6b36647ce516ebd17d71ff146cdb0a(
    *,
    custom_layers: typing.Optional[typing.Sequence[builtins.str]] = None,
    political_view: typing.Optional[builtins.str] = None,
    style: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522080d3c60480841661cc7e6354c6a046c67827c1c3c24ea02bb01b372fa83e(
    *,
    data_source: typing.Optional[builtins.str] = None,
    data_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlaceIndexPropsMixin.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    index_name: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241d744e50c85cea0b61f26b9b9025a5d79d7e828e7db35b3c19a44dad04ea35(
    props: typing.Union[CfnPlaceIndexMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38b8b806c0a1e1f5fdabf9cb6c71e2e6d8821be427e9f73d6df20a9667cde3a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00ed7d34266035ae227fc24c565b4d3b55a8a50cca3e0280e28e98063fbdcd9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10f88e6abbb475201c2a956d8a4366504c1d7b3d3071a004c5a09a936c90344(
    *,
    intended_use: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3da25d608eb03573bc26b77127a996d3930b10a1b7f81195e7ec72e59388c10(
    *,
    calculator_name: typing.Optional[builtins.str] = None,
    data_source: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5146f411a6ed3c91a3f2c4064a22e8b9c950ce2a16a02102f8eccf9c3d28293(
    props: typing.Union[CfnRouteCalculatorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc4c7f36d452041572605f5efca219339a91e820dcc6417612416d3b3efd9a4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f038d510a241f5665a475e1ef1aec1a81d06b3ae27ed86fe2e32924d7763484(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb9ff3cef3e36741b2cde4387fc2e63637ee26042299a175f08f66c194cd9c6(
    *,
    consumer_arn: typing.Optional[builtins.str] = None,
    tracker_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210dd32b254c5a51e79ab674b357bda6c02181a9a791fff7e0b16bf1ef51ef05(
    props: typing.Union[CfnTrackerConsumerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a775008e27efd90b43eee6ce0240f3f664d9d8459efbd920059b73d2229263d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf1ac131f4c3c04f6fe07acef5bae5c97cc5bf90a50de8b8ccb93356608e0c4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb8a1bb8f7dbe12e2cdabc96bc9c69dd616df5cca7769ba81f65be433913637(
    *,
    description: typing.Optional[builtins.str] = None,
    event_bridge_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_key_enable_geospatial_queries: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    position_filtering: typing.Optional[builtins.str] = None,
    pricing_plan: typing.Optional[builtins.str] = None,
    pricing_plan_data_source: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tracker_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f1ace89ac5e08711cc5b877bafe86721690e8798a482ee4eaa37b3b1178c69(
    props: typing.Union[CfnTrackerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41aced6a6b3ce9ffeb78df5d8cad32c0e546b4245d751011752bba5f288e86e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bb65bd4abb916ab747dac18c1068ee796ce1ece419c0a258ae9d78f063a599(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
