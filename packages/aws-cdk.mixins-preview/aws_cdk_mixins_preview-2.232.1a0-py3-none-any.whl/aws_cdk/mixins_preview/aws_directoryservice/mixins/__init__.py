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
    jsii_type="@aws-cdk/mixins-preview.aws_directoryservice.mixins.CfnMicrosoftADMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_alias": "createAlias",
        "edition": "edition",
        "enable_sso": "enableSso",
        "name": "name",
        "password": "password",
        "short_name": "shortName",
        "vpc_settings": "vpcSettings",
    },
)
class CfnMicrosoftADMixinProps:
    def __init__(
        self,
        *,
        create_alias: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        edition: typing.Optional[builtins.str] = None,
        enable_sso: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        short_name: typing.Optional[builtins.str] = None,
        vpc_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMicrosoftADPropsMixin.VpcSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMicrosoftADPropsMixin.

        :param create_alias: Specifies an alias for a directory and assigns the alias to the directory. The alias is used to construct the access URL for the directory, such as ``http://<alias>.awsapps.com`` . By default, CloudFormation does not create an alias. .. epigraph:: After an alias has been created, it cannot be deleted or reused, so this operation should only be used when absolutely necessary.
        :param edition: AWS Managed Microsoft AD is available in two editions: ``Standard`` and ``Enterprise`` . ``Enterprise`` is the default.
        :param enable_sso: Whether to enable single sign-on for a Microsoft Active Directory in AWS . Single sign-on allows users in your directory to access certain AWS services from a computer joined to the directory without having to enter their credentials separately. If you don't specify a value, CloudFormation disables single sign-on by default.
        :param name: The fully qualified domain name for the AWS Managed Microsoft AD directory, such as ``corp.example.com`` . This name will resolve inside your VPC only. It does not need to be publicly resolvable.
        :param password: The password for the default administrative user named ``Admin`` . If you need to change the password for the administrator account, see the `ResetUserPassword <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_ResetUserPassword.html>`_ API call in the *Directory Service API Reference* .
        :param short_name: The NetBIOS name for your domain, such as ``CORP`` . If you don't specify a NetBIOS name, it will default to the first part of your directory DNS. For example, ``CORP`` for the directory DNS ``corp.example.com`` .
        :param vpc_settings: Specifies the VPC settings of the Microsoft AD directory server in AWS .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_directoryservice import mixins as directoryservice_mixins
            
            cfn_microsoft_aDMixin_props = directoryservice_mixins.CfnMicrosoftADMixinProps(
                create_alias=False,
                edition="edition",
                enable_sso=False,
                name="name",
                password="password",
                short_name="shortName",
                vpc_settings=directoryservice_mixins.CfnMicrosoftADPropsMixin.VpcSettingsProperty(
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca3914b99a40eb1cc909722ace4ce8cba09645ceb0a392e168f3b90fdad4700a)
            check_type(argname="argument create_alias", value=create_alias, expected_type=type_hints["create_alias"])
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument enable_sso", value=enable_sso, expected_type=type_hints["enable_sso"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument short_name", value=short_name, expected_type=type_hints["short_name"])
            check_type(argname="argument vpc_settings", value=vpc_settings, expected_type=type_hints["vpc_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create_alias is not None:
            self._values["create_alias"] = create_alias
        if edition is not None:
            self._values["edition"] = edition
        if enable_sso is not None:
            self._values["enable_sso"] = enable_sso
        if name is not None:
            self._values["name"] = name
        if password is not None:
            self._values["password"] = password
        if short_name is not None:
            self._values["short_name"] = short_name
        if vpc_settings is not None:
            self._values["vpc_settings"] = vpc_settings

    @builtins.property
    def create_alias(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies an alias for a directory and assigns the alias to the directory.

        The alias is used to construct the access URL for the directory, such as ``http://<alias>.awsapps.com`` . By default, CloudFormation does not create an alias.
        .. epigraph::

           After an alias has been created, it cannot be deleted or reused, so this operation should only be used when absolutely necessary.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html#cfn-directoryservice-microsoftad-createalias
        '''
        result = self._values.get("create_alias")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def edition(self) -> typing.Optional[builtins.str]:
        '''AWS Managed Microsoft AD is available in two editions: ``Standard`` and ``Enterprise`` .

        ``Enterprise`` is the default.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html#cfn-directoryservice-microsoftad-edition
        '''
        result = self._values.get("edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_sso(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to enable single sign-on for a Microsoft Active Directory in AWS .

        Single sign-on allows users in your directory to access certain AWS services from a computer joined to the directory without having to enter their credentials separately. If you don't specify a value, CloudFormation disables single sign-on by default.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html#cfn-directoryservice-microsoftad-enablesso
        '''
        result = self._values.get("enable_sso")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified domain name for the AWS Managed Microsoft AD directory, such as ``corp.example.com`` . This name will resolve inside your VPC only. It does not need to be publicly resolvable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html#cfn-directoryservice-microsoftad-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password for the default administrative user named ``Admin`` .

        If you need to change the password for the administrator account, see the `ResetUserPassword <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_ResetUserPassword.html>`_ API call in the *Directory Service API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html#cfn-directoryservice-microsoftad-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def short_name(self) -> typing.Optional[builtins.str]:
        '''The NetBIOS name for your domain, such as ``CORP`` .

        If you don't specify a NetBIOS name, it will default to the first part of your directory DNS. For example, ``CORP`` for the directory DNS ``corp.example.com`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html#cfn-directoryservice-microsoftad-shortname
        '''
        result = self._values.get("short_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMicrosoftADPropsMixin.VpcSettingsProperty"]]:
        '''Specifies the VPC settings of the Microsoft AD directory server in AWS .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html#cfn-directoryservice-microsoftad-vpcsettings
        '''
        result = self._values.get("vpc_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMicrosoftADPropsMixin.VpcSettingsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMicrosoftADMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMicrosoftADPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_directoryservice.mixins.CfnMicrosoftADPropsMixin",
):
    '''The ``AWS::DirectoryService::MicrosoftAD`` resource specifies a Microsoft Active Directory in AWS so that your directory users and groups can access the AWS Management Console and AWS applications using their existing credentials.

    For more information, see `AWS Managed Microsoft AD <https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_microsoft_ad.html>`_ in the *Directory Service Admin Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-microsoftad.html
    :cloudformationResource: AWS::DirectoryService::MicrosoftAD
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_directoryservice import mixins as directoryservice_mixins
        
        cfn_microsoft_aDProps_mixin = directoryservice_mixins.CfnMicrosoftADPropsMixin(directoryservice_mixins.CfnMicrosoftADMixinProps(
            create_alias=False,
            edition="edition",
            enable_sso=False,
            name="name",
            password="password",
            short_name="shortName",
            vpc_settings=directoryservice_mixins.CfnMicrosoftADPropsMixin.VpcSettingsProperty(
                subnet_ids=["subnetIds"],
                vpc_id="vpcId"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMicrosoftADMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DirectoryService::MicrosoftAD``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55141a2e6ea6ae8586767e36fce6f4755eef30eec91260d3c4edd67c648ea82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a159b7054fc8bef43ccc60f98509a8fe47375c3200d06349c41a1ef56ee33e87)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690207c45ee7bbae64e0777b37f27f61a4d957e2636344001b2631324dd6d0dc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMicrosoftADMixinProps:
        return typing.cast(CfnMicrosoftADMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_directoryservice.mixins.CfnMicrosoftADPropsMixin.VpcSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"subnet_ids": "subnetIds", "vpc_id": "vpcId"},
    )
    class VpcSettingsProperty:
        def __init__(
            self,
            *,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains VPC information for the `CreateDirectory <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_CreateDirectory.html>`_ or `CreateMicrosoftAD <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_CreateMicrosoftAD.html>`_ operation.

            :param subnet_ids: The identifiers of the subnets for the directory servers. The two subnets must be in different Availability Zones. Directory Service specifies a directory server and a DNS server in each of these subnets.
            :param vpc_id: The identifier of the VPC in which to create the directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-directoryservice-microsoftad-vpcsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_directoryservice import mixins as directoryservice_mixins
                
                vpc_settings_property = directoryservice_mixins.CfnMicrosoftADPropsMixin.VpcSettingsProperty(
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a1bebdb479ce5ae86fd7d2960a43f1c76132cdbba2ce8e0b8ba8de8803612d6)
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the subnets for the directory servers.

            The two subnets must be in different Availability Zones. Directory Service specifies a directory server and a DNS server in each of these subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-directoryservice-microsoftad-vpcsettings.html#cfn-directoryservice-microsoftad-vpcsettings-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the VPC in which to create the directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-directoryservice-microsoftad-vpcsettings.html#cfn-directoryservice-microsoftad-vpcsettings-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_directoryservice.mixins.CfnSimpleADMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_alias": "createAlias",
        "description": "description",
        "enable_sso": "enableSso",
        "name": "name",
        "password": "password",
        "short_name": "shortName",
        "size": "size",
        "vpc_settings": "vpcSettings",
    },
)
class CfnSimpleADMixinProps:
    def __init__(
        self,
        *,
        create_alias: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_sso: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        short_name: typing.Optional[builtins.str] = None,
        size: typing.Optional[builtins.str] = None,
        vpc_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSimpleADPropsMixin.VpcSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSimpleADPropsMixin.

        :param create_alias: If set to ``true`` , specifies an alias for a directory and assigns the alias to the directory. The alias is used to construct the access URL for the directory, such as ``http://<alias>.awsapps.com`` . By default, this property is set to ``false`` . .. epigraph:: After an alias has been created, it cannot be deleted or reused, so this operation should only be used when absolutely necessary.
        :param description: A description for the directory.
        :param enable_sso: Whether to enable single sign-on for a directory. If you don't specify a value, CloudFormation disables single sign-on by default.
        :param name: The fully qualified name for the directory, such as ``corp.example.com`` .
        :param password: The password for the directory administrator. The directory creation process creates a directory administrator account with the user name ``Administrator`` and this password. If you need to change the password for the administrator account, see the `ResetUserPassword <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_ResetUserPassword.html>`_ API call in the *Directory Service API Reference* .
        :param short_name: The NetBIOS name of the directory, such as ``CORP`` .
        :param size: The size of the directory. For valid values, see `CreateDirectory <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_CreateDirectory.html>`_ in the *Directory Service API Reference* .
        :param vpc_settings: A `DirectoryVpcSettings <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_DirectoryVpcSettings.html>`_ object that contains additional information for the operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_directoryservice import mixins as directoryservice_mixins
            
            cfn_simple_aDMixin_props = directoryservice_mixins.CfnSimpleADMixinProps(
                create_alias=False,
                description="description",
                enable_sso=False,
                name="name",
                password="password",
                short_name="shortName",
                size="size",
                vpc_settings=directoryservice_mixins.CfnSimpleADPropsMixin.VpcSettingsProperty(
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3e4a338bbd78fedfa0aa9949ab009f54d63e10f0ac9f446cbd92709c08a2e6)
            check_type(argname="argument create_alias", value=create_alias, expected_type=type_hints["create_alias"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_sso", value=enable_sso, expected_type=type_hints["enable_sso"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument short_name", value=short_name, expected_type=type_hints["short_name"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument vpc_settings", value=vpc_settings, expected_type=type_hints["vpc_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create_alias is not None:
            self._values["create_alias"] = create_alias
        if description is not None:
            self._values["description"] = description
        if enable_sso is not None:
            self._values["enable_sso"] = enable_sso
        if name is not None:
            self._values["name"] = name
        if password is not None:
            self._values["password"] = password
        if short_name is not None:
            self._values["short_name"] = short_name
        if size is not None:
            self._values["size"] = size
        if vpc_settings is not None:
            self._values["vpc_settings"] = vpc_settings

    @builtins.property
    def create_alias(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If set to ``true`` , specifies an alias for a directory and assigns the alias to the directory.

        The alias is used to construct the access URL for the directory, such as ``http://<alias>.awsapps.com`` . By default, this property is set to ``false`` .
        .. epigraph::

           After an alias has been created, it cannot be deleted or reused, so this operation should only be used when absolutely necessary.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html#cfn-directoryservice-simplead-createalias
        '''
        result = self._values.get("create_alias")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the directory.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html#cfn-directoryservice-simplead-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_sso(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to enable single sign-on for a directory.

        If you don't specify a value, CloudFormation disables single sign-on by default.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html#cfn-directoryservice-simplead-enablesso
        '''
        result = self._values.get("enable_sso")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name for the directory, such as ``corp.example.com`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html#cfn-directoryservice-simplead-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password for the directory administrator.

        The directory creation process creates a directory administrator account with the user name ``Administrator`` and this password.

        If you need to change the password for the administrator account, see the `ResetUserPassword <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_ResetUserPassword.html>`_ API call in the *Directory Service API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html#cfn-directoryservice-simplead-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def short_name(self) -> typing.Optional[builtins.str]:
        '''The NetBIOS name of the directory, such as ``CORP`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html#cfn-directoryservice-simplead-shortname
        '''
        result = self._values.get("short_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[builtins.str]:
        '''The size of the directory.

        For valid values, see `CreateDirectory <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_CreateDirectory.html>`_ in the *Directory Service API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html#cfn-directoryservice-simplead-size
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimpleADPropsMixin.VpcSettingsProperty"]]:
        '''A `DirectoryVpcSettings <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_DirectoryVpcSettings.html>`_ object that contains additional information for the operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html#cfn-directoryservice-simplead-vpcsettings
        '''
        result = self._values.get("vpc_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSimpleADPropsMixin.VpcSettingsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimpleADMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSimpleADPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_directoryservice.mixins.CfnSimpleADPropsMixin",
):
    '''The ``AWS::DirectoryService::SimpleAD`` resource specifies an Directory Service Simple Active Directory ( Simple AD ) in AWS so that your directory users and groups can access the AWS Management Console and AWS applications using their existing credentials.

    Simple AD is a Microsoft Active Directory–compatible directory. For more information, see `Simple Active Directory <https://docs.aws.amazon.com/directoryservice/latest/admin-guide/directory_simple_ad.html>`_ in the *Directory Service Admin Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-directoryservice-simplead.html
    :cloudformationResource: AWS::DirectoryService::SimpleAD
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_directoryservice import mixins as directoryservice_mixins
        
        cfn_simple_aDProps_mixin = directoryservice_mixins.CfnSimpleADPropsMixin(directoryservice_mixins.CfnSimpleADMixinProps(
            create_alias=False,
            description="description",
            enable_sso=False,
            name="name",
            password="password",
            short_name="shortName",
            size="size",
            vpc_settings=directoryservice_mixins.CfnSimpleADPropsMixin.VpcSettingsProperty(
                subnet_ids=["subnetIds"],
                vpc_id="vpcId"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSimpleADMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DirectoryService::SimpleAD``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23767488c84a5933f3d7ac5a39b09855201b02aab66101e6fad68eeb265c8a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29f73cb5b6f0284549a019c07a79c56d30b62bf6d6c7f1ee4d5707caf204d578)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fc8abc4698c0b11cdc405917a14c710ad474671e082a0b13ead35d9a322acf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSimpleADMixinProps:
        return typing.cast(CfnSimpleADMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_directoryservice.mixins.CfnSimpleADPropsMixin.VpcSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"subnet_ids": "subnetIds", "vpc_id": "vpcId"},
    )
    class VpcSettingsProperty:
        def __init__(
            self,
            *,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains VPC information for the `CreateDirectory <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_CreateDirectory.html>`_ or `CreateMicrosoftAD <https://docs.aws.amazon.com/directoryservice/latest/devguide/API_CreateMicrosoftAD.html>`_ operation.

            :param subnet_ids: The identifiers of the subnets for the directory servers. The two subnets must be in different Availability Zones. Directory Service specifies a directory server and a DNS server in each of these subnets.
            :param vpc_id: The identifier of the VPC in which to create the directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-directoryservice-simplead-vpcsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_directoryservice import mixins as directoryservice_mixins
                
                vpc_settings_property = directoryservice_mixins.CfnSimpleADPropsMixin.VpcSettingsProperty(
                    subnet_ids=["subnetIds"],
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__140276b331b89683204a84178ef8cafcc5e0bec8afb9d2b9d47a9201dd7f6a6d)
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identifiers of the subnets for the directory servers.

            The two subnets must be in different Availability Zones. Directory Service specifies a directory server and a DNS server in each of these subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-directoryservice-simplead-vpcsettings.html#cfn-directoryservice-simplead-vpcsettings-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the VPC in which to create the directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-directoryservice-simplead-vpcsettings.html#cfn-directoryservice-simplead-vpcsettings-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnMicrosoftADMixinProps",
    "CfnMicrosoftADPropsMixin",
    "CfnSimpleADMixinProps",
    "CfnSimpleADPropsMixin",
]

publication.publish()

def _typecheckingstub__ca3914b99a40eb1cc909722ace4ce8cba09645ceb0a392e168f3b90fdad4700a(
    *,
    create_alias: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    edition: typing.Optional[builtins.str] = None,
    enable_sso: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    short_name: typing.Optional[builtins.str] = None,
    vpc_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMicrosoftADPropsMixin.VpcSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55141a2e6ea6ae8586767e36fce6f4755eef30eec91260d3c4edd67c648ea82(
    props: typing.Union[CfnMicrosoftADMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a159b7054fc8bef43ccc60f98509a8fe47375c3200d06349c41a1ef56ee33e87(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690207c45ee7bbae64e0777b37f27f61a4d957e2636344001b2631324dd6d0dc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a1bebdb479ce5ae86fd7d2960a43f1c76132cdbba2ce8e0b8ba8de8803612d6(
    *,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3e4a338bbd78fedfa0aa9949ab009f54d63e10f0ac9f446cbd92709c08a2e6(
    *,
    create_alias: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_sso: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    short_name: typing.Optional[builtins.str] = None,
    size: typing.Optional[builtins.str] = None,
    vpc_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSimpleADPropsMixin.VpcSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23767488c84a5933f3d7ac5a39b09855201b02aab66101e6fad68eeb265c8a1(
    props: typing.Union[CfnSimpleADMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f73cb5b6f0284549a019c07a79c56d30b62bf6d6c7f1ee4d5707caf204d578(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fc8abc4698c0b11cdc405917a14c710ad474671e082a0b13ead35d9a322acf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140276b331b89683204a84178ef8cafcc5e0bec8afb9d2b9d47a9201dd7f6a6d(
    *,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
