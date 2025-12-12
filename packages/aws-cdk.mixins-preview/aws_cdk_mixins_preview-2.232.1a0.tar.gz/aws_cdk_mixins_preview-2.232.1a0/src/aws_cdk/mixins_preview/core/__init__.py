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

from .._jsii import *

import constructs as _constructs_77d1e7e8


class ConstructSelector(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.core.ConstructSelector",
):
    '''(experimental) Selects constructs from a construct tree based on various criteria.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import core
        
        construct_selector = core.ConstructSelector()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> "IConstructSelector":
        '''(experimental) Selects all constructs in the tree.

        :stability: experimental
        '''
        return typing.cast("IConstructSelector", jsii.sinvoke(cls, "all", []))

    @jsii.member(jsii_name="byId")
    @builtins.classmethod
    def by_id(cls, pattern: builtins.str) -> "IConstructSelector":
        '''(experimental) Selects constructs whose construct IDs match a pattern.

        Uses glob like matching.

        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ecb9b3435499cf874e1852a6007ff39e2b20b6e8b1c7938a7f546c2eecc20a)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("IConstructSelector", jsii.sinvoke(cls, "byId", [pattern]))

    @jsii.member(jsii_name="byPath")
    @builtins.classmethod
    def by_path(cls, pattern: builtins.str) -> "IConstructSelector":
        '''(experimental) Selects constructs whose construct paths match a pattern.

        Uses glob like matching.

        :param pattern: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138eabf7bbb5b921e828154628718eedde5579aa501b40d412769111b090e213)
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        return typing.cast("IConstructSelector", jsii.sinvoke(cls, "byPath", [pattern]))

    @jsii.member(jsii_name="cfnResource")
    @builtins.classmethod
    def cfn_resource(cls) -> "IConstructSelector":
        '''(experimental) Selects CfnResource constructs or the default CfnResource child.

        :stability: experimental
        '''
        return typing.cast("IConstructSelector", jsii.sinvoke(cls, "cfnResource", []))

    @jsii.member(jsii_name="onlyItself")
    @builtins.classmethod
    def only_itself(cls) -> "IConstructSelector":
        '''(experimental) Selects only the provided construct.

        :stability: experimental
        '''
        return typing.cast("IConstructSelector", jsii.sinvoke(cls, "onlyItself", []))

    @jsii.member(jsii_name="resourcesOfType")
    @builtins.classmethod
    def resources_of_type(cls, *types: builtins.str) -> "IConstructSelector":
        '''(experimental) Selects constructs of a specific type.

        :param types: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bde46462d50ad507b3877bb465052cacbe2732041bc267d9b3579c53a2c296a)
            check_type(argname="argument types", value=types, expected_type=typing.Tuple[type_hints["types"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IConstructSelector", jsii.sinvoke(cls, "resourcesOfType", [*types]))


@jsii.interface(jsii_type="@aws-cdk/mixins-preview.core.IConstructSelector")
class IConstructSelector(typing_extensions.Protocol):
    '''(experimental) Selects constructs from a construct tree.

    :stability: experimental
    '''

    @jsii.member(jsii_name="select")
    def select(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> typing.List[_constructs_77d1e7e8.IConstruct]:
        '''(experimental) Selects constructs from the given scope based on the selector's criteria.

        :param scope: -

        :stability: experimental
        '''
        ...


class _IConstructSelectorProxy:
    '''(experimental) Selects constructs from a construct tree.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/mixins-preview.core.IConstructSelector"

    @jsii.member(jsii_name="select")
    def select(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> typing.List[_constructs_77d1e7e8.IConstruct]:
        '''(experimental) Selects constructs from the given scope based on the selector's criteria.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8deb82db82b1303a807da9ba4c02d7a6a36de577b3ef646533a1e2490b56db3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(typing.List[_constructs_77d1e7e8.IConstruct], jsii.invoke(self, "select", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConstructSelector).__jsii_proxy_class__ = lambda : _IConstructSelectorProxy


@jsii.interface(jsii_type="@aws-cdk/mixins-preview.core.IMixin")
class IMixin(typing_extensions.Protocol):
    '''(experimental) A mixin is a reusable piece of functionality that can be applied to constructs to add behavior, properties, or modify existing functionality without inheritance.

    :stability: experimental
    '''

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''(experimental) Applies the mixin functionality to the target construct.

        :param construct: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''(experimental) Determines whether this mixin can be applied to the given construct.

        :param construct: -

        :stability: experimental
        '''
        ...


class _IMixinProxy:
    '''(experimental) A mixin is a reusable piece of functionality that can be applied to constructs to add behavior, properties, or modify existing functionality without inheritance.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/mixins-preview.core.IMixin"

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''(experimental) Applies the mixin functionality to the target construct.

        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0dafd92f2dd0bd7cad15120adac33f3a1e10c6b2a52a39c83e427550b3d24da)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''(experimental) Determines whether this mixin can be applied to the given construct.

        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e13747ac5e3cf5f881eab36e445d711c3b99d832254fd84f9ddef6375bafadea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMixin).__jsii_proxy_class__ = lambda : _IMixinProxy


@jsii.implements(IMixin)
class Mixin(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/mixins-preview.core.Mixin",
):
    '''(experimental) Abstract base class for mixins that provides default implementations.

    :stability: experimental
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="isMixin")
    @builtins.classmethod
    def is_mixin(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Checks if ``x`` is a Mixin.

        :param x: Any object.

        :return: true if ``x`` is an object created from a class which extends ``Mixin``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a739b0af07ba29566ed5b0afde63d74a64ad456ece03c91eb972b1474ce7fd61)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isMixin", [x]))

    @jsii.member(jsii_name="applyTo")
    @abc.abstractmethod
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''(experimental) Applies the mixin functionality to the target construct.

        :param construct: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="supports")
    def supports(self, _construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''(experimental) Determines whether this mixin can be applied to the given construct.

        :param _construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bf779e4c0a9dfec403233c473d7472c4699c146c2695f563e0ebd30d16bf389)
            check_type(argname="argument _construct", value=_construct, expected_type=type_hints["_construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [_construct]))


class _MixinProxy(Mixin):
    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        construct: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''(experimental) Applies the mixin functionality to the target construct.

        :param construct: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc06e214132588e622c9ba1faa42a4f7b897ad8641baa9b079a8120417f8a24)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Mixin).__jsii_proxy_class__ = lambda : _MixinProxy


class MixinApplicator(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.core.MixinApplicator",
):
    '''(experimental) Applies mixins to constructs.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import core
        
        # construct_selector: core.IConstructSelector
        
        mixin_applicator = core.MixinApplicator(self, construct_selector)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        selector: typing.Optional[IConstructSelector] = None,
    ) -> None:
        '''
        :param scope: -
        :param selector: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776712f720cc5712a713f8d7fd71794812baff2ced30303f04e9ad6971b20ee2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
        jsii.create(self.__class__, self, [scope, selector])

    @jsii.member(jsii_name="apply")
    def apply(self, *mixins: IMixin) -> "MixinApplicator":
        '''(experimental) Applies a mixin to selected constructs.

        :param mixins: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f47d8a0813b7cc8c8e36ecc4340b3d3c4cd49e6fd9ec4f3108a3af08b734ff)
            check_type(argname="argument mixins", value=mixins, expected_type=typing.Tuple[type_hints["mixins"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("MixinApplicator", jsii.invoke(self, "apply", [*mixins]))

    @jsii.member(jsii_name="mustApply")
    def must_apply(self, *mixins: IMixin) -> "MixinApplicator":
        '''(experimental) Applies a mixin and requires that it be applied to all constructs.

        :param mixins: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e360c01a79208aa4469f9bb06c5ca9c806be31e8429b9b4da783e943db541dc9)
            check_type(argname="argument mixins", value=mixins, expected_type=typing.Tuple[type_hints["mixins"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("MixinApplicator", jsii.invoke(self, "mustApply", [*mixins]))


class Mixins(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/mixins-preview.core.Mixins"):
    '''(experimental) Main entry point for applying mixins.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import core
        
        mixins = core.Mixins()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        selector: typing.Optional[IConstructSelector] = None,
    ) -> MixinApplicator:
        '''(experimental) Creates a MixinApplicator for the given scope.

        :param scope: -
        :param selector: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc44e70390b06cf24e238a21785063f42f14da8c6a1cb8225f5d315930b432b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument selector", value=selector, expected_type=type_hints["selector"])
        return typing.cast(MixinApplicator, jsii.sinvoke(cls, "of", [scope, selector]))


__all__ = [
    "ConstructSelector",
    "IConstructSelector",
    "IMixin",
    "Mixin",
    "MixinApplicator",
    "Mixins",
]

publication.publish()

def _typecheckingstub__f6ecb9b3435499cf874e1852a6007ff39e2b20b6e8b1c7938a7f546c2eecc20a(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138eabf7bbb5b921e828154628718eedde5579aa501b40d412769111b090e213(
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bde46462d50ad507b3877bb465052cacbe2732041bc267d9b3579c53a2c296a(
    *types: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8deb82db82b1303a807da9ba4c02d7a6a36de577b3ef646533a1e2490b56db3(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0dafd92f2dd0bd7cad15120adac33f3a1e10c6b2a52a39c83e427550b3d24da(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e13747ac5e3cf5f881eab36e445d711c3b99d832254fd84f9ddef6375bafadea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a739b0af07ba29566ed5b0afde63d74a64ad456ece03c91eb972b1474ce7fd61(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bf779e4c0a9dfec403233c473d7472c4699c146c2695f563e0ebd30d16bf389(
    _construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc06e214132588e622c9ba1faa42a4f7b897ad8641baa9b079a8120417f8a24(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776712f720cc5712a713f8d7fd71794812baff2ced30303f04e9ad6971b20ee2(
    scope: _constructs_77d1e7e8.IConstruct,
    selector: typing.Optional[IConstructSelector] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f47d8a0813b7cc8c8e36ecc4340b3d3c4cd49e6fd9ec4f3108a3af08b734ff(
    *mixins: IMixin,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e360c01a79208aa4469f9bb06c5ca9c806be31e8429b9b4da783e943db541dc9(
    *mixins: IMixin,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc44e70390b06cf24e238a21785063f42f14da8c6a1cb8225f5d315930b432b(
    scope: _constructs_77d1e7e8.IConstruct,
    selector: typing.Optional[IConstructSelector] = None,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IConstructSelector, IMixin]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
