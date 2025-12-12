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
    jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connectivity_info": "connectivityInfo",
        "environment_name": "environmentName",
        "hosts": "hosts",
        "initial_vlans": "initialVlans",
        "kms_key_id": "kmsKeyId",
        "license_info": "licenseInfo",
        "service_access_security_groups": "serviceAccessSecurityGroups",
        "service_access_subnet_id": "serviceAccessSubnetId",
        "site_id": "siteId",
        "tags": "tags",
        "terms_accepted": "termsAccepted",
        "vcf_hostnames": "vcfHostnames",
        "vcf_version": "vcfVersion",
        "vpc_id": "vpcId",
    },
)
class CfnEnvironmentMixinProps:
    def __init__(
        self,
        *,
        connectivity_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.ConnectivityInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        environment_name: typing.Optional[builtins.str] = None,
        hosts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.HostInfoForCreateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        initial_vlans: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlansProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        license_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.LicenseInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_access_security_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.ServiceAccessSecurityGroupsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_access_subnet_id: typing.Optional[builtins.str] = None,
        site_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        terms_accepted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        vcf_hostnames: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.VcfHostnamesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vcf_version: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEnvironmentPropsMixin.

        :param connectivity_info: The connectivity configuration for the environment. Amazon EVS requires that you specify two route server peer IDs. During environment creation, the route server endpoints peer with the NSX uplink VLAN for connectivity to the NSX overlay network.
        :param environment_name: The name of the environment.
        :param hosts: Required for environment resource creation.
        :param initial_vlans: .. epigraph:: Amazon EVS is in public preview release and is subject to change. The initial VLAN subnets for the environment. Amazon EVS VLAN subnets have a minimum CIDR block size of /28 and a maximum size of /24. Amazon EVS VLAN subnet CIDR blocks must not overlap with other subnets in the VPC. Required for environment resource creation.
        :param kms_key_id: The AWS KMS key ID that AWS Secrets Manager uses to encrypt secrets that are associated with the environment. These secrets contain the VCF credentials that are needed to install vCenter Server, NSX, and SDDC Manager. By default, Amazon EVS use the AWS Secrets Manager managed key ``aws/secretsmanager`` . You can also specify a customer managed key.
        :param license_info: The license information that Amazon EVS requires to create an environment. Amazon EVS requires two license keys: a VCF solution key and a vSAN license key. The VCF solution key must cover a minimum of 256 cores. The vSAN license key must provide at least 110 TiB of vSAN capacity.
        :param service_access_security_groups: The security groups that allow traffic between the Amazon EVS control plane and your VPC for service access. If a security group is not specified, Amazon EVS uses the default security group in your account for service access.
        :param service_access_subnet_id: The subnet that is used to establish connectivity between the Amazon EVS control plane and VPC. Amazon EVS uses this subnet to perform validations and create the environment.
        :param site_id: The Broadcom Site ID that is associated with your Amazon EVS environment. Amazon EVS uses the Broadcom Site ID that you provide to meet Broadcom VCF license usage reporting requirements for Amazon EVS.
        :param tags: Metadata that assists with categorization and organization. Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.
        :param terms_accepted: Customer confirmation that the customer has purchased and will continue to maintain the required number of VCF software licenses to cover all physical processor cores in the Amazon EVS environment. Information about your VCF software in Amazon EVS will be shared with Broadcom to verify license compliance. Amazon EVS does not validate license keys. To validate license keys, visit the Broadcom support portal.
        :param vcf_hostnames: The DNS hostnames to be used by the VCF management appliances in your environment. For environment creation to be successful, each hostname entry must resolve to a domain name that you've registered in your DNS service of choice and configured in the DHCP option set of your VPC. DNS hostnames cannot be changed after environment creation has started.
        :param vcf_version: The VCF version of the environment.
        :param vpc_id: The VPC associated with the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
            
            cfn_environment_mixin_props = evs_mixins.CfnEnvironmentMixinProps(
                connectivity_info=evs_mixins.CfnEnvironmentPropsMixin.ConnectivityInfoProperty(
                    private_route_server_peerings=["privateRouteServerPeerings"]
                ),
                environment_name="environmentName",
                hosts=[evs_mixins.CfnEnvironmentPropsMixin.HostInfoForCreateProperty(
                    dedicated_host_id="dedicatedHostId",
                    host_name="hostName",
                    instance_type="instanceType",
                    key_name="keyName",
                    placement_group_id="placementGroupId"
                )],
                initial_vlans=evs_mixins.CfnEnvironmentPropsMixin.InitialVlansProperty(
                    edge_vTep=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    expansion_vlan1=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    expansion_vlan2=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    hcx=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    hcx_network_acl_id="hcxNetworkAclId",
                    is_hcx_public=False,
                    nsx_up_link=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    vmk_management=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    vm_management=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    v_motion=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    v_san=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    v_tep=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    )
                ),
                kms_key_id="kmsKeyId",
                license_info=evs_mixins.CfnEnvironmentPropsMixin.LicenseInfoProperty(
                    solution_key="solutionKey",
                    vsan_key="vsanKey"
                ),
                service_access_security_groups=evs_mixins.CfnEnvironmentPropsMixin.ServiceAccessSecurityGroupsProperty(
                    security_groups=["securityGroups"]
                ),
                service_access_subnet_id="serviceAccessSubnetId",
                site_id="siteId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                terms_accepted=False,
                vcf_hostnames=evs_mixins.CfnEnvironmentPropsMixin.VcfHostnamesProperty(
                    cloud_builder="cloudBuilder",
                    nsx="nsx",
                    nsx_edge1="nsxEdge1",
                    nsx_edge2="nsxEdge2",
                    nsx_manager1="nsxManager1",
                    nsx_manager2="nsxManager2",
                    nsx_manager3="nsxManager3",
                    sddc_manager="sddcManager",
                    v_center="vCenter"
                ),
                vcf_version="vcfVersion",
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15be037537aea6a43a4e18f8edf2ae3b22a39317dc8fba52e8d931596a9dd57)
            check_type(argname="argument connectivity_info", value=connectivity_info, expected_type=type_hints["connectivity_info"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument initial_vlans", value=initial_vlans, expected_type=type_hints["initial_vlans"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument license_info", value=license_info, expected_type=type_hints["license_info"])
            check_type(argname="argument service_access_security_groups", value=service_access_security_groups, expected_type=type_hints["service_access_security_groups"])
            check_type(argname="argument service_access_subnet_id", value=service_access_subnet_id, expected_type=type_hints["service_access_subnet_id"])
            check_type(argname="argument site_id", value=site_id, expected_type=type_hints["site_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument terms_accepted", value=terms_accepted, expected_type=type_hints["terms_accepted"])
            check_type(argname="argument vcf_hostnames", value=vcf_hostnames, expected_type=type_hints["vcf_hostnames"])
            check_type(argname="argument vcf_version", value=vcf_version, expected_type=type_hints["vcf_version"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connectivity_info is not None:
            self._values["connectivity_info"] = connectivity_info
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if hosts is not None:
            self._values["hosts"] = hosts
        if initial_vlans is not None:
            self._values["initial_vlans"] = initial_vlans
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if license_info is not None:
            self._values["license_info"] = license_info
        if service_access_security_groups is not None:
            self._values["service_access_security_groups"] = service_access_security_groups
        if service_access_subnet_id is not None:
            self._values["service_access_subnet_id"] = service_access_subnet_id
        if site_id is not None:
            self._values["site_id"] = site_id
        if tags is not None:
            self._values["tags"] = tags
        if terms_accepted is not None:
            self._values["terms_accepted"] = terms_accepted
        if vcf_hostnames is not None:
            self._values["vcf_hostnames"] = vcf_hostnames
        if vcf_version is not None:
            self._values["vcf_version"] = vcf_version
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def connectivity_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ConnectivityInfoProperty"]]:
        '''The connectivity configuration for the environment.

        Amazon EVS requires that you specify two route server peer IDs. During environment creation, the route server endpoints peer with the NSX uplink VLAN for connectivity to the NSX overlay network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-connectivityinfo
        '''
        result = self._values.get("connectivity_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ConnectivityInfoProperty"]], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-environmentname
        '''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosts(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.HostInfoForCreateProperty"]]]]:
        '''Required for environment resource creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-hosts
        '''
        result = self._values.get("hosts")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.HostInfoForCreateProperty"]]]], result)

    @builtins.property
    def initial_vlans(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlansProperty"]]:
        '''.. epigraph::

   Amazon EVS is in public preview release and is subject to change.

        The initial VLAN subnets for the environment. Amazon EVS VLAN subnets have a minimum CIDR block size of /28 and a maximum size of /24. Amazon EVS VLAN subnet CIDR blocks must not overlap with other subnets in the VPC.

        Required for environment resource creation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-initialvlans
        '''
        result = self._values.get("initial_vlans")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlansProperty"]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The AWS KMS key ID that AWS Secrets Manager uses to encrypt secrets that are associated with the environment.

        These secrets contain the VCF credentials that are needed to install vCenter Server, NSX, and SDDC Manager.

        By default, Amazon EVS use the AWS Secrets Manager managed key ``aws/secretsmanager`` . You can also specify a customer managed key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.LicenseInfoProperty"]]:
        '''The license information that Amazon EVS requires to create an environment.

        Amazon EVS requires two license keys: a VCF solution key and a vSAN license key. The VCF solution key must cover a minimum of 256 cores. The vSAN license key must provide at least 110 TiB of vSAN capacity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-licenseinfo
        '''
        result = self._values.get("license_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.LicenseInfoProperty"]], result)

    @builtins.property
    def service_access_security_groups(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ServiceAccessSecurityGroupsProperty"]]:
        '''The security groups that allow traffic between the Amazon EVS control plane and your VPC for service access.

        If a security group is not specified, Amazon EVS uses the default security group in your account for service access.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-serviceaccesssecuritygroups
        '''
        result = self._values.get("service_access_security_groups")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.ServiceAccessSecurityGroupsProperty"]], result)

    @builtins.property
    def service_access_subnet_id(self) -> typing.Optional[builtins.str]:
        '''The subnet that is used to establish connectivity between the Amazon EVS control plane and VPC.

        Amazon EVS uses this subnet to perform validations and create the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-serviceaccesssubnetid
        '''
        result = self._values.get("service_access_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site_id(self) -> typing.Optional[builtins.str]:
        '''The Broadcom Site ID that is associated with your Amazon EVS environment.

        Amazon EVS uses the Broadcom Site ID that you provide to meet Broadcom VCF license usage reporting requirements for Amazon EVS.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-siteid
        '''
        result = self._values.get("site_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that assists with categorization and organization.

        Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def terms_accepted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Customer confirmation that the customer has purchased and will continue to maintain the required number of VCF software licenses to cover all physical processor cores in the Amazon EVS environment.

        Information about your VCF software in Amazon EVS will be shared with Broadcom to verify license compliance. Amazon EVS does not validate license keys. To validate license keys, visit the Broadcom support portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-termsaccepted
        '''
        result = self._values.get("terms_accepted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def vcf_hostnames(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.VcfHostnamesProperty"]]:
        '''The DNS hostnames to be used by the VCF management appliances in your environment.

        For environment creation to be successful, each hostname entry must resolve to a domain name that you've registered in your DNS service of choice and configured in the DHCP option set of your VPC. DNS hostnames cannot be changed after environment creation has started.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-vcfhostnames
        '''
        result = self._values.get("vcf_hostnames")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.VcfHostnamesProperty"]], result)

    @builtins.property
    def vcf_version(self) -> typing.Optional[builtins.str]:
        '''The VCF version of the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-vcfversion
        '''
        result = self._values.get("vcf_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The VPC associated with the environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html#cfn-evs-environment-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin",
):
    '''Creates an Amazon EVS environment that runs VCF software, such as SDDC Manager, NSX Manager, and vCenter Server.

    During environment creation, Amazon EVS performs validations on DNS settings, provisions VLAN subnets and hosts, and deploys the supplied version of VCF.

    It can take several hours to create an environment. After the deployment completes, you can configure VCF in the vSphere user interface according to your needs.
    .. epigraph::

       You cannot use the ``dedicatedHostId`` and ``placementGroupId`` parameters together in the same ``CreateEnvironment`` action. This results in a ``ValidationException`` response.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-evs-environment.html
    :cloudformationResource: AWS::EVS::Environment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
        
        cfn_environment_props_mixin = evs_mixins.CfnEnvironmentPropsMixin(evs_mixins.CfnEnvironmentMixinProps(
            connectivity_info=evs_mixins.CfnEnvironmentPropsMixin.ConnectivityInfoProperty(
                private_route_server_peerings=["privateRouteServerPeerings"]
            ),
            environment_name="environmentName",
            hosts=[evs_mixins.CfnEnvironmentPropsMixin.HostInfoForCreateProperty(
                dedicated_host_id="dedicatedHostId",
                host_name="hostName",
                instance_type="instanceType",
                key_name="keyName",
                placement_group_id="placementGroupId"
            )],
            initial_vlans=evs_mixins.CfnEnvironmentPropsMixin.InitialVlansProperty(
                edge_vTep=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                ),
                expansion_vlan1=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                ),
                expansion_vlan2=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                ),
                hcx=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                ),
                hcx_network_acl_id="hcxNetworkAclId",
                is_hcx_public=False,
                nsx_up_link=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                ),
                vmk_management=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                ),
                vm_management=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                ),
                v_motion=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                ),
                v_san=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                ),
                v_tep=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                )
            ),
            kms_key_id="kmsKeyId",
            license_info=evs_mixins.CfnEnvironmentPropsMixin.LicenseInfoProperty(
                solution_key="solutionKey",
                vsan_key="vsanKey"
            ),
            service_access_security_groups=evs_mixins.CfnEnvironmentPropsMixin.ServiceAccessSecurityGroupsProperty(
                security_groups=["securityGroups"]
            ),
            service_access_subnet_id="serviceAccessSubnetId",
            site_id="siteId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            terms_accepted=False,
            vcf_hostnames=evs_mixins.CfnEnvironmentPropsMixin.VcfHostnamesProperty(
                cloud_builder="cloudBuilder",
                nsx="nsx",
                nsx_edge1="nsxEdge1",
                nsx_edge2="nsxEdge2",
                nsx_manager1="nsxManager1",
                nsx_manager2="nsxManager2",
                nsx_manager3="nsxManager3",
                sddc_manager="sddcManager",
                v_center="vCenter"
            ),
            vcf_version="vcfVersion",
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EVS::Environment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f435dc4d1f4633cd9317f6012f4cb7a7a138c3c0f121490c15e1aae805c9a7ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ee36a836a0d805f28ad5ba284c0da8e5133825329e2fd461b58d33b17df92cb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36ca5f1f78a893e1a10444793f0250969e9756efa78a364a473ea7c48ca7fbd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentMixinProps:
        return typing.cast(CfnEnvironmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin.CheckProperty",
        jsii_struct_bases=[],
        name_mapping={
            "impaired_since": "impairedSince",
            "result": "result",
            "type": "type",
        },
    )
    class CheckProperty:
        def __init__(
            self,
            *,
            impaired_since: typing.Optional[builtins.str] = None,
            result: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A check on the environment to identify environment health and validate VMware VCF licensing compliance.

            :param impaired_since: The time when environment health began to be impaired.
            :param result: The check result.
            :param type: The check type. Amazon EVS performs the following checks. - ``KEY_REUSE`` : checks that the VCF license key is not used by another Amazon EVS environment. This check fails if a used license is added to the environment. - ``KEY_COVERAGE`` : checks that your VCF license key allocates sufficient vCPU cores for all deployed hosts. The check fails when any assigned hosts in the EVS environment are not covered by license keys, or when any unassigned hosts cannot be covered by available vCPU cores in keys. - ``REACHABILITY`` : checks that the Amazon EVS control plane has a persistent connection to SDDC Manager. If Amazon EVS cannot reach the environment, this check fails. - ``HOST_COUNT`` : Checks that your environment has a minimum of 4 hosts, which is a requirement for VCF 5.2.1. If this check fails, you will need to add hosts so that your environment meets this minimum requirement. Amazon EVS only supports environments with 4-16 hosts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-check.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
                
                check_property = evs_mixins.CfnEnvironmentPropsMixin.CheckProperty(
                    impaired_since="impairedSince",
                    result="result",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3ad56686e7e02c24473d4bbd79b441727d587e14df253d61ecf952aa2525473)
                check_type(argname="argument impaired_since", value=impaired_since, expected_type=type_hints["impaired_since"])
                check_type(argname="argument result", value=result, expected_type=type_hints["result"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if impaired_since is not None:
                self._values["impaired_since"] = impaired_since
            if result is not None:
                self._values["result"] = result
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def impaired_since(self) -> typing.Optional[builtins.str]:
            '''The time when environment health began to be impaired.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-check.html#cfn-evs-environment-check-impairedsince
            '''
            result = self._values.get("impaired_since")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def result(self) -> typing.Optional[builtins.str]:
            '''The check result.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-check.html#cfn-evs-environment-check-result
            '''
            result = self._values.get("result")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The check type. Amazon EVS performs the following checks.

            - ``KEY_REUSE`` : checks that the VCF license key is not used by another Amazon EVS environment. This check fails if a used license is added to the environment.
            - ``KEY_COVERAGE`` : checks that your VCF license key allocates sufficient vCPU cores for all deployed hosts. The check fails when any assigned hosts in the EVS environment are not covered by license keys, or when any unassigned hosts cannot be covered by available vCPU cores in keys.
            - ``REACHABILITY`` : checks that the Amazon EVS control plane has a persistent connection to SDDC Manager. If Amazon EVS cannot reach the environment, this check fails.
            - ``HOST_COUNT`` : Checks that your environment has a minimum of 4 hosts, which is a requirement for VCF 5.2.1.

            If this check fails, you will need to add hosts so that your environment meets this minimum requirement. Amazon EVS only supports environments with 4-16 hosts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-check.html#cfn-evs-environment-check-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CheckProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin.ConnectivityInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"private_route_server_peerings": "privateRouteServerPeerings"},
    )
    class ConnectivityInfoProperty:
        def __init__(
            self,
            *,
            private_route_server_peerings: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The connectivity configuration for the environment.

            Amazon EVS requires that you specify two route server peer IDs. During environment creation, the route server endpoints peer with the NSX uplink VLAN for connectivity to the NSX overlay network.

            :param private_route_server_peerings: The unique IDs for private route server peers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-connectivityinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
                
                connectivity_info_property = evs_mixins.CfnEnvironmentPropsMixin.ConnectivityInfoProperty(
                    private_route_server_peerings=["privateRouteServerPeerings"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e0a85d9a47f21f0a3c4d22b4515c4b706c134a92776677d90f93a958c6f0f00)
                check_type(argname="argument private_route_server_peerings", value=private_route_server_peerings, expected_type=type_hints["private_route_server_peerings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if private_route_server_peerings is not None:
                self._values["private_route_server_peerings"] = private_route_server_peerings

        @builtins.property
        def private_route_server_peerings(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The unique IDs for private route server peers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-connectivityinfo.html#cfn-evs-environment-connectivityinfo-privaterouteserverpeerings
            '''
            result = self._values.get("private_route_server_peerings")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectivityInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin.HostInfoForCreateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dedicated_host_id": "dedicatedHostId",
            "host_name": "hostName",
            "instance_type": "instanceType",
            "key_name": "keyName",
            "placement_group_id": "placementGroupId",
        },
    )
    class HostInfoForCreateProperty:
        def __init__(
            self,
            *,
            dedicated_host_id: typing.Optional[builtins.str] = None,
            host_name: typing.Optional[builtins.str] = None,
            instance_type: typing.Optional[builtins.str] = None,
            key_name: typing.Optional[builtins.str] = None,
            placement_group_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a host.

            .. epigraph::

               You cannot use ``dedicatedHostId`` and ``placementGroupId`` together in the same ``HostInfoForCreate`` object. This results in a ``ValidationException`` response.

            :param dedicated_host_id: The unique ID of the Amazon EC2 Dedicated Host.
            :param host_name: The DNS hostname of the host. DNS hostnames for hosts must be unique across Amazon EVS environments and within VCF.
            :param instance_type: The EC2 instance type that represents the host.
            :param key_name: The name of the SSH key that is used to access the host.
            :param placement_group_id: The unique ID of the placement group where the host is placed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-hostinfoforcreate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
                
                host_info_for_create_property = evs_mixins.CfnEnvironmentPropsMixin.HostInfoForCreateProperty(
                    dedicated_host_id="dedicatedHostId",
                    host_name="hostName",
                    instance_type="instanceType",
                    key_name="keyName",
                    placement_group_id="placementGroupId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b002593b8c4635492aea2ef701b20f3cd4107066aefc01d7098b23234ee8d052)
                check_type(argname="argument dedicated_host_id", value=dedicated_host_id, expected_type=type_hints["dedicated_host_id"])
                check_type(argname="argument host_name", value=host_name, expected_type=type_hints["host_name"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
                check_type(argname="argument placement_group_id", value=placement_group_id, expected_type=type_hints["placement_group_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dedicated_host_id is not None:
                self._values["dedicated_host_id"] = dedicated_host_id
            if host_name is not None:
                self._values["host_name"] = host_name
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if key_name is not None:
                self._values["key_name"] = key_name
            if placement_group_id is not None:
                self._values["placement_group_id"] = placement_group_id

        @builtins.property
        def dedicated_host_id(self) -> typing.Optional[builtins.str]:
            '''The unique ID of the Amazon EC2 Dedicated Host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-hostinfoforcreate.html#cfn-evs-environment-hostinfoforcreate-dedicatedhostid
            '''
            result = self._values.get("dedicated_host_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_name(self) -> typing.Optional[builtins.str]:
            '''The DNS hostname of the host.

            DNS hostnames for hosts must be unique across Amazon EVS environments and within VCF.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-hostinfoforcreate.html#cfn-evs-environment-hostinfoforcreate-hostname
            '''
            result = self._values.get("host_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The EC2 instance type that represents the host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-hostinfoforcreate.html#cfn-evs-environment-hostinfoforcreate-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_name(self) -> typing.Optional[builtins.str]:
            '''The name of the SSH key that is used to access the host.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-hostinfoforcreate.html#cfn-evs-environment-hostinfoforcreate-keyname
            '''
            result = self._values.get("key_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def placement_group_id(self) -> typing.Optional[builtins.str]:
            '''The unique ID of the placement group where the host is placed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-hostinfoforcreate.html#cfn-evs-environment-hostinfoforcreate-placementgroupid
            '''
            result = self._values.get("placement_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostInfoForCreateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr": "cidr"},
    )
    class InitialVlanInfoProperty:
        def __init__(self, *, cidr: typing.Optional[builtins.str] = None) -> None:
            '''An object that represents an initial VLAN subnet for the Amazon EVS environment.

            Amazon EVS creates initial VLAN subnets when you first create the environment. Amazon EVS creates the following 10 VLAN subnets: host management VLAN, vMotion VLAN, vSAN VLAN, VTEP VLAN, Edge VTEP VLAN, Management VM VLAN, HCX uplink VLAN, NSX uplink VLAN, expansion VLAN 1, expansion VLAN 2.
            .. epigraph::

               For each Amazon EVS VLAN subnet, you must specify a non-overlapping CIDR block. Amazon EVS VLAN subnets have a minimum CIDR block size of /28 and a maximum size of /24.

            :param cidr: The CIDR block that you provide to create an Amazon EVS VLAN subnet. Amazon EVS VLAN subnets have a minimum CIDR block size of /28 and a maximum size of /24. Amazon EVS VLAN subnet CIDR blocks must not overlap with other subnets in the VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlaninfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
                
                initial_vlan_info_property = evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                    cidr="cidr"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b44bb9188e32bd8bc3555e4f548aa9336c9ef5b8cd9f10f7d3f0a80bd898215c)
                check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidr is not None:
                self._values["cidr"] = cidr

        @builtins.property
        def cidr(self) -> typing.Optional[builtins.str]:
            '''The CIDR block that you provide to create an Amazon EVS VLAN subnet.

            Amazon EVS VLAN subnets have a minimum CIDR block size of /28 and a maximum size of /24. Amazon EVS VLAN subnet CIDR blocks must not overlap with other subnets in the VPC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlaninfo.html#cfn-evs-environment-initialvlaninfo-cidr
            '''
            result = self._values.get("cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitialVlanInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin.InitialVlansProperty",
        jsii_struct_bases=[],
        name_mapping={
            "edge_v_tep": "edgeVTep",
            "expansion_vlan1": "expansionVlan1",
            "expansion_vlan2": "expansionVlan2",
            "hcx": "hcx",
            "hcx_network_acl_id": "hcxNetworkAclId",
            "is_hcx_public": "isHcxPublic",
            "nsx_up_link": "nsxUpLink",
            "vmk_management": "vmkManagement",
            "vm_management": "vmManagement",
            "v_motion": "vMotion",
            "v_san": "vSan",
            "v_tep": "vTep",
        },
    )
    class InitialVlansProperty:
        def __init__(
            self,
            *,
            edge_v_tep: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            expansion_vlan1: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            expansion_vlan2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hcx: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hcx_network_acl_id: typing.Optional[builtins.str] = None,
            is_hcx_public: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            nsx_up_link: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vmk_management: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vm_management: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            v_motion: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            v_san: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            v_tep: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEnvironmentPropsMixin.InitialVlanInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The initial VLAN subnets for the environment.

            Amazon EVS VLAN subnets have a minimum CIDR block size of /28 and a maximum size of /24. Amazon EVS VLAN subnet CIDR blocks must not overlap with other subnets in the VPC.

            :param edge_v_tep: The edge VTEP VLAN subnet. This VLAN subnet manages traffic flowing between the internal network and external networks, including internet access and other site connections.
            :param expansion_vlan1: An additional VLAN subnet that can be used to extend VCF capabilities once configured. For example, you can configure an expansion VLAN subnet to use NSX Federation for centralized management and synchronization of multiple NSX deployments across different locations.
            :param expansion_vlan2: An additional VLAN subnet that can be used to extend VCF capabilities once configured. For example, you can configure an expansion VLAN subnet to use NSX Federation for centralized management and synchronization of multiple NSX deployments across different locations.
            :param hcx: The HCX VLAN subnet. This VLAN subnet allows the HCX Interconnnect (IX) and HCX Network Extension (NE) to reach their peers and enable HCX Service Mesh creation. If you plan to use a public HCX VLAN subnet, the following requirements must be met: - Must have a /28 netmask and be allocated from the IPAM public pool. Required for HCX internet access configuration. - The HCX public VLAN CIDR block must be added to the VPC as a secondary CIDR block. - Must have at least two Elastic IP addresses to be allocated from the public IPAM pool for HCX components.
            :param hcx_network_acl_id: A unique ID for a network access control list that the HCX VLAN uses. Required when ``isHcxPublic`` is set to ``true`` .
            :param is_hcx_public: Determines if the HCX VLAN that Amazon EVS provisions is public or private.
            :param nsx_up_link: The NSX uplink VLAN subnet. This VLAN subnet allows connectivity to the NSX overlay network.
            :param vmk_management: The host VMkernel management VLAN subnet. This VLAN subnet carries traffic for managing ESXi hosts and communicating with VMware vCenter Server.
            :param vm_management: The VM management VLAN subnet. This VLAN subnet carries traffic for vSphere virtual machines.
            :param v_motion: The vMotion VLAN subnet. This VLAN subnet carries traffic for vSphere vMotion.
            :param v_san: The vSAN VLAN subnet. This VLAN subnet carries the communication between ESXi hosts to implement a vSAN shared storage pool.
            :param v_tep: The VTEP VLAN subnet. This VLAN subnet handles internal network traffic between virtual machines within a VCF instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
                
                initial_vlans_property = evs_mixins.CfnEnvironmentPropsMixin.InitialVlansProperty(
                    edge_vTep=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    expansion_vlan1=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    expansion_vlan2=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    hcx=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    hcx_network_acl_id="hcxNetworkAclId",
                    is_hcx_public=False,
                    nsx_up_link=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    vmk_management=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    vm_management=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    v_motion=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    v_san=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    ),
                    v_tep=evs_mixins.CfnEnvironmentPropsMixin.InitialVlanInfoProperty(
                        cidr="cidr"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdcf472862c6042febe5d0074e24ad073e94c026428fd4f4c3b070668f7adca7)
                check_type(argname="argument edge_v_tep", value=edge_v_tep, expected_type=type_hints["edge_v_tep"])
                check_type(argname="argument expansion_vlan1", value=expansion_vlan1, expected_type=type_hints["expansion_vlan1"])
                check_type(argname="argument expansion_vlan2", value=expansion_vlan2, expected_type=type_hints["expansion_vlan2"])
                check_type(argname="argument hcx", value=hcx, expected_type=type_hints["hcx"])
                check_type(argname="argument hcx_network_acl_id", value=hcx_network_acl_id, expected_type=type_hints["hcx_network_acl_id"])
                check_type(argname="argument is_hcx_public", value=is_hcx_public, expected_type=type_hints["is_hcx_public"])
                check_type(argname="argument nsx_up_link", value=nsx_up_link, expected_type=type_hints["nsx_up_link"])
                check_type(argname="argument vmk_management", value=vmk_management, expected_type=type_hints["vmk_management"])
                check_type(argname="argument vm_management", value=vm_management, expected_type=type_hints["vm_management"])
                check_type(argname="argument v_motion", value=v_motion, expected_type=type_hints["v_motion"])
                check_type(argname="argument v_san", value=v_san, expected_type=type_hints["v_san"])
                check_type(argname="argument v_tep", value=v_tep, expected_type=type_hints["v_tep"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if edge_v_tep is not None:
                self._values["edge_v_tep"] = edge_v_tep
            if expansion_vlan1 is not None:
                self._values["expansion_vlan1"] = expansion_vlan1
            if expansion_vlan2 is not None:
                self._values["expansion_vlan2"] = expansion_vlan2
            if hcx is not None:
                self._values["hcx"] = hcx
            if hcx_network_acl_id is not None:
                self._values["hcx_network_acl_id"] = hcx_network_acl_id
            if is_hcx_public is not None:
                self._values["is_hcx_public"] = is_hcx_public
            if nsx_up_link is not None:
                self._values["nsx_up_link"] = nsx_up_link
            if vmk_management is not None:
                self._values["vmk_management"] = vmk_management
            if vm_management is not None:
                self._values["vm_management"] = vm_management
            if v_motion is not None:
                self._values["v_motion"] = v_motion
            if v_san is not None:
                self._values["v_san"] = v_san
            if v_tep is not None:
                self._values["v_tep"] = v_tep

        @builtins.property
        def edge_v_tep(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''The edge VTEP VLAN subnet.

            This VLAN subnet manages traffic flowing between the internal network and external networks, including internet access and other site connections.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-edgevtep
            '''
            result = self._values.get("edge_v_tep")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        @builtins.property
        def expansion_vlan1(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''An additional VLAN subnet that can be used to extend VCF capabilities once configured.

            For example, you can configure an expansion VLAN subnet to use NSX Federation for centralized management and synchronization of multiple NSX deployments across different locations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-expansionvlan1
            '''
            result = self._values.get("expansion_vlan1")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        @builtins.property
        def expansion_vlan2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''An additional VLAN subnet that can be used to extend VCF capabilities once configured.

            For example, you can configure an expansion VLAN subnet to use NSX Federation for centralized management and synchronization of multiple NSX deployments across different locations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-expansionvlan2
            '''
            result = self._values.get("expansion_vlan2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        @builtins.property
        def hcx(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''The HCX VLAN subnet.

            This VLAN subnet allows the HCX Interconnnect (IX) and HCX Network Extension (NE) to reach their peers and enable HCX Service Mesh creation.

            If you plan to use a public HCX VLAN subnet, the following requirements must be met:

            - Must have a /28 netmask and be allocated from the IPAM public pool. Required for HCX internet access configuration.
            - The HCX public VLAN CIDR block must be added to the VPC as a secondary CIDR block.
            - Must have at least two Elastic IP addresses to be allocated from the public IPAM pool for HCX components.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-hcx
            '''
            result = self._values.get("hcx")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        @builtins.property
        def hcx_network_acl_id(self) -> typing.Optional[builtins.str]:
            '''A unique ID for a network access control list that the HCX VLAN uses.

            Required when ``isHcxPublic`` is set to ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-hcxnetworkaclid
            '''
            result = self._values.get("hcx_network_acl_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_hcx_public(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Determines if the HCX VLAN that Amazon EVS provisions is public or private.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-ishcxpublic
            '''
            result = self._values.get("is_hcx_public")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def nsx_up_link(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''The NSX uplink VLAN subnet.

            This VLAN subnet allows connectivity to the NSX overlay network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-nsxuplink
            '''
            result = self._values.get("nsx_up_link")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        @builtins.property
        def vmk_management(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''The host VMkernel management VLAN subnet.

            This VLAN subnet carries traffic for managing ESXi hosts and communicating with VMware vCenter Server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-vmkmanagement
            '''
            result = self._values.get("vmk_management")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        @builtins.property
        def vm_management(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''The VM management VLAN subnet.

            This VLAN subnet carries traffic for vSphere virtual machines.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-vmmanagement
            '''
            result = self._values.get("vm_management")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        @builtins.property
        def v_motion(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''The vMotion VLAN subnet.

            This VLAN subnet carries traffic for vSphere vMotion.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-vmotion
            '''
            result = self._values.get("v_motion")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        @builtins.property
        def v_san(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''The vSAN VLAN subnet.

            This VLAN subnet carries the communication between ESXi hosts to implement a vSAN shared storage pool.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-vsan
            '''
            result = self._values.get("v_san")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        @builtins.property
        def v_tep(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]]:
            '''The VTEP VLAN subnet.

            This VLAN subnet handles internal network traffic between virtual machines within a VCF instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-initialvlans.html#cfn-evs-environment-initialvlans-vtep
            '''
            result = self._values.get("v_tep")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEnvironmentPropsMixin.InitialVlanInfoProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitialVlansProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin.LicenseInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"solution_key": "solutionKey", "vsan_key": "vsanKey"},
    )
    class LicenseInfoProperty:
        def __init__(
            self,
            *,
            solution_key: typing.Optional[builtins.str] = None,
            vsan_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The license information that Amazon EVS requires to create an environment.

            Amazon EVS requires two license keys: a VCF solution key and a vSAN license key.

            :param solution_key: The VCF solution key. This license unlocks VMware VCF product features, including vSphere, NSX, SDDC Manager, and vCenter Server. The VCF solution key must cover a minimum of 256 cores.
            :param vsan_key: The VSAN license key. This license unlocks vSAN features. The vSAN license key must provide at least 110 TiB of vSAN capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-licenseinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
                
                license_info_property = evs_mixins.CfnEnvironmentPropsMixin.LicenseInfoProperty(
                    solution_key="solutionKey",
                    vsan_key="vsanKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ed76be830d25e0028acd6c743688620f64c011ffba2f02fce3e710562309087)
                check_type(argname="argument solution_key", value=solution_key, expected_type=type_hints["solution_key"])
                check_type(argname="argument vsan_key", value=vsan_key, expected_type=type_hints["vsan_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if solution_key is not None:
                self._values["solution_key"] = solution_key
            if vsan_key is not None:
                self._values["vsan_key"] = vsan_key

        @builtins.property
        def solution_key(self) -> typing.Optional[builtins.str]:
            '''The VCF solution key.

            This license unlocks VMware VCF product features, including vSphere, NSX, SDDC Manager, and vCenter Server. The VCF solution key must cover a minimum of 256 cores.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-licenseinfo.html#cfn-evs-environment-licenseinfo-solutionkey
            '''
            result = self._values.get("solution_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vsan_key(self) -> typing.Optional[builtins.str]:
            '''The VSAN license key.

            This license unlocks vSAN features. The vSAN license key must provide at least 110 TiB of vSAN capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-licenseinfo.html#cfn-evs-environment-licenseinfo-vsankey
            '''
            result = self._values.get("vsan_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LicenseInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin.SecretProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn"},
    )
    class SecretProperty:
        def __init__(self, *, secret_arn: typing.Optional[builtins.str] = None) -> None:
            '''A managed secret that contains the credentials for installing vCenter Server, NSX, and SDDC Manager.

            During environment creation, the Amazon EVS control plane uses AWS Secrets Manager to create, encrypt, validate, and store secrets. If you choose to delete your environment, Amazon EVS also deletes the secrets that are associated with your environment. Amazon EVS does not provide managed rotation of secrets. We recommend that you rotate secrets regularly to ensure that secrets are not long-lived.

            :param secret_arn: The Amazon Resource Name (ARN) of the secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-secret.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
                
                secret_property = evs_mixins.CfnEnvironmentPropsMixin.SecretProperty(
                    secret_arn="secretArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b83ae6bc2c2d9a74e1ee10212e3500a6958dd1a66d61aa6135ce0c351f5e74a0)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the secret.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-secret.html#cfn-evs-environment-secret-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin.ServiceAccessSecurityGroupsProperty",
        jsii_struct_bases=[],
        name_mapping={"security_groups": "securityGroups"},
    )
    class ServiceAccessSecurityGroupsProperty:
        def __init__(
            self,
            *,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The security groups that allow traffic between the Amazon EVS control plane and your VPC for Amazon EVS service access.

            If a security group is not specified, Amazon EVS uses the default security group in your account for service access.

            :param security_groups: The security groups that allow service access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-serviceaccesssecuritygroups.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
                
                service_access_security_groups_property = evs_mixins.CfnEnvironmentPropsMixin.ServiceAccessSecurityGroupsProperty(
                    security_groups=["securityGroups"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62a9abb13865f2320f06ea9ee11d5b931d422421b4910ac20fc738e7d040a21b)
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_groups is not None:
                self._values["security_groups"] = security_groups

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The security groups that allow service access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-serviceaccesssecuritygroups.html#cfn-evs-environment-serviceaccesssecuritygroups-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceAccessSecurityGroupsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_evs.mixins.CfnEnvironmentPropsMixin.VcfHostnamesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_builder": "cloudBuilder",
            "nsx": "nsx",
            "nsx_edge1": "nsxEdge1",
            "nsx_edge2": "nsxEdge2",
            "nsx_manager1": "nsxManager1",
            "nsx_manager2": "nsxManager2",
            "nsx_manager3": "nsxManager3",
            "sddc_manager": "sddcManager",
            "v_center": "vCenter",
        },
    )
    class VcfHostnamesProperty:
        def __init__(
            self,
            *,
            cloud_builder: typing.Optional[builtins.str] = None,
            nsx: typing.Optional[builtins.str] = None,
            nsx_edge1: typing.Optional[builtins.str] = None,
            nsx_edge2: typing.Optional[builtins.str] = None,
            nsx_manager1: typing.Optional[builtins.str] = None,
            nsx_manager2: typing.Optional[builtins.str] = None,
            nsx_manager3: typing.Optional[builtins.str] = None,
            sddc_manager: typing.Optional[builtins.str] = None,
            v_center: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The DNS hostnames that Amazon EVS uses to install VMware vCenter Server, NSX, SDDC Manager, and Cloud Builder.

            Each hostname must be unique, and resolve to a domain name that you've registered in your DNS service of choice. Hostnames cannot be changed.

            VMware VCF requires the deployment of two NSX Edge nodes, and three NSX Manager virtual machines.

            :param cloud_builder: The hostname for VMware Cloud Builder.
            :param nsx: The VMware NSX hostname.
            :param nsx_edge1: The hostname for the first NSX Edge node.
            :param nsx_edge2: The hostname for the second NSX Edge node.
            :param nsx_manager1: The hostname for the first VMware NSX Manager virtual machine (VM).
            :param nsx_manager2: The hostname for the second VMware NSX Manager virtual machine (VM).
            :param nsx_manager3: The hostname for the third VMware NSX Manager virtual machine (VM).
            :param sddc_manager: The hostname for SDDC Manager.
            :param v_center: The VMware vCenter hostname.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_evs import mixins as evs_mixins
                
                vcf_hostnames_property = evs_mixins.CfnEnvironmentPropsMixin.VcfHostnamesProperty(
                    cloud_builder="cloudBuilder",
                    nsx="nsx",
                    nsx_edge1="nsxEdge1",
                    nsx_edge2="nsxEdge2",
                    nsx_manager1="nsxManager1",
                    nsx_manager2="nsxManager2",
                    nsx_manager3="nsxManager3",
                    sddc_manager="sddcManager",
                    v_center="vCenter"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b421ecd8667c7fcb6f25e1935f8325c0a634ee3fda676a20980c4e78d7ef0162)
                check_type(argname="argument cloud_builder", value=cloud_builder, expected_type=type_hints["cloud_builder"])
                check_type(argname="argument nsx", value=nsx, expected_type=type_hints["nsx"])
                check_type(argname="argument nsx_edge1", value=nsx_edge1, expected_type=type_hints["nsx_edge1"])
                check_type(argname="argument nsx_edge2", value=nsx_edge2, expected_type=type_hints["nsx_edge2"])
                check_type(argname="argument nsx_manager1", value=nsx_manager1, expected_type=type_hints["nsx_manager1"])
                check_type(argname="argument nsx_manager2", value=nsx_manager2, expected_type=type_hints["nsx_manager2"])
                check_type(argname="argument nsx_manager3", value=nsx_manager3, expected_type=type_hints["nsx_manager3"])
                check_type(argname="argument sddc_manager", value=sddc_manager, expected_type=type_hints["sddc_manager"])
                check_type(argname="argument v_center", value=v_center, expected_type=type_hints["v_center"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_builder is not None:
                self._values["cloud_builder"] = cloud_builder
            if nsx is not None:
                self._values["nsx"] = nsx
            if nsx_edge1 is not None:
                self._values["nsx_edge1"] = nsx_edge1
            if nsx_edge2 is not None:
                self._values["nsx_edge2"] = nsx_edge2
            if nsx_manager1 is not None:
                self._values["nsx_manager1"] = nsx_manager1
            if nsx_manager2 is not None:
                self._values["nsx_manager2"] = nsx_manager2
            if nsx_manager3 is not None:
                self._values["nsx_manager3"] = nsx_manager3
            if sddc_manager is not None:
                self._values["sddc_manager"] = sddc_manager
            if v_center is not None:
                self._values["v_center"] = v_center

        @builtins.property
        def cloud_builder(self) -> typing.Optional[builtins.str]:
            '''The hostname for VMware Cloud Builder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html#cfn-evs-environment-vcfhostnames-cloudbuilder
            '''
            result = self._values.get("cloud_builder")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nsx(self) -> typing.Optional[builtins.str]:
            '''The VMware NSX hostname.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html#cfn-evs-environment-vcfhostnames-nsx
            '''
            result = self._values.get("nsx")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nsx_edge1(self) -> typing.Optional[builtins.str]:
            '''The hostname for the first NSX Edge node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html#cfn-evs-environment-vcfhostnames-nsxedge1
            '''
            result = self._values.get("nsx_edge1")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nsx_edge2(self) -> typing.Optional[builtins.str]:
            '''The hostname for the second NSX Edge node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html#cfn-evs-environment-vcfhostnames-nsxedge2
            '''
            result = self._values.get("nsx_edge2")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nsx_manager1(self) -> typing.Optional[builtins.str]:
            '''The hostname for the first VMware NSX Manager virtual machine (VM).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html#cfn-evs-environment-vcfhostnames-nsxmanager1
            '''
            result = self._values.get("nsx_manager1")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nsx_manager2(self) -> typing.Optional[builtins.str]:
            '''The hostname for the second VMware NSX Manager virtual machine (VM).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html#cfn-evs-environment-vcfhostnames-nsxmanager2
            '''
            result = self._values.get("nsx_manager2")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nsx_manager3(self) -> typing.Optional[builtins.str]:
            '''The hostname for the third VMware NSX Manager virtual machine (VM).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html#cfn-evs-environment-vcfhostnames-nsxmanager3
            '''
            result = self._values.get("nsx_manager3")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sddc_manager(self) -> typing.Optional[builtins.str]:
            '''The hostname for SDDC Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html#cfn-evs-environment-vcfhostnames-sddcmanager
            '''
            result = self._values.get("sddc_manager")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def v_center(self) -> typing.Optional[builtins.str]:
            '''The VMware vCenter hostname.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-evs-environment-vcfhostnames.html#cfn-evs-environment-vcfhostnames-vcenter
            '''
            result = self._values.get("v_center")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VcfHostnamesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnEnvironmentMixinProps",
    "CfnEnvironmentPropsMixin",
]

publication.publish()

def _typecheckingstub__f15be037537aea6a43a4e18f8edf2ae3b22a39317dc8fba52e8d931596a9dd57(
    *,
    connectivity_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.ConnectivityInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment_name: typing.Optional[builtins.str] = None,
    hosts: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.HostInfoForCreateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    initial_vlans: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlansProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    license_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.LicenseInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_access_security_groups: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.ServiceAccessSecurityGroupsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_access_subnet_id: typing.Optional[builtins.str] = None,
    site_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    terms_accepted: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    vcf_hostnames: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.VcfHostnamesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vcf_version: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f435dc4d1f4633cd9317f6012f4cb7a7a138c3c0f121490c15e1aae805c9a7ea(
    props: typing.Union[CfnEnvironmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee36a836a0d805f28ad5ba284c0da8e5133825329e2fd461b58d33b17df92cb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36ca5f1f78a893e1a10444793f0250969e9756efa78a364a473ea7c48ca7fbd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ad56686e7e02c24473d4bbd79b441727d587e14df253d61ecf952aa2525473(
    *,
    impaired_since: typing.Optional[builtins.str] = None,
    result: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0a85d9a47f21f0a3c4d22b4515c4b706c134a92776677d90f93a958c6f0f00(
    *,
    private_route_server_peerings: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b002593b8c4635492aea2ef701b20f3cd4107066aefc01d7098b23234ee8d052(
    *,
    dedicated_host_id: typing.Optional[builtins.str] = None,
    host_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    key_name: typing.Optional[builtins.str] = None,
    placement_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b44bb9188e32bd8bc3555e4f548aa9336c9ef5b8cd9f10f7d3f0a80bd898215c(
    *,
    cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcf472862c6042febe5d0074e24ad073e94c026428fd4f4c3b070668f7adca7(
    *,
    edge_v_tep: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    expansion_vlan1: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    expansion_vlan2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hcx: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hcx_network_acl_id: typing.Optional[builtins.str] = None,
    is_hcx_public: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    nsx_up_link: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vmk_management: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vm_management: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    v_motion: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    v_san: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    v_tep: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEnvironmentPropsMixin.InitialVlanInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed76be830d25e0028acd6c743688620f64c011ffba2f02fce3e710562309087(
    *,
    solution_key: typing.Optional[builtins.str] = None,
    vsan_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83ae6bc2c2d9a74e1ee10212e3500a6958dd1a66d61aa6135ce0c351f5e74a0(
    *,
    secret_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a9abb13865f2320f06ea9ee11d5b931d422421b4910ac20fc738e7d040a21b(
    *,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b421ecd8667c7fcb6f25e1935f8325c0a634ee3fda676a20980c4e78d7ef0162(
    *,
    cloud_builder: typing.Optional[builtins.str] = None,
    nsx: typing.Optional[builtins.str] = None,
    nsx_edge1: typing.Optional[builtins.str] = None,
    nsx_edge2: typing.Optional[builtins.str] = None,
    nsx_manager1: typing.Optional[builtins.str] = None,
    nsx_manager2: typing.Optional[builtins.str] = None,
    nsx_manager3: typing.Optional[builtins.str] = None,
    sddc_manager: typing.Optional[builtins.str] = None,
    v_center: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
