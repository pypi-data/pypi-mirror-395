r'''
# cdk-vpc-module

cdk-vpc-module construct library is an open-source extension of the AWS Cloud Development Kit (AWS CDK) to deploy configurable aws vpc  and its individual components in less than 50 lines of code and human readable configuration which can be managed by pull requests!

## :sparkles: Features

* :white_check_mark: Option to configure custom IPv4 CIDR(10.10.0.0/24)
* :white_check_mark: VPC Peering with  route table entry
* :white_check_mark: Configurable NACL as per subnet group
* :white_check_mark: NATGateway as per availabilityZones

Using cdk a vpc can be deployed using the following sample code snippet:

```python
import { Network } from "@smallcase/cdk-vpc-module/lib/constructs/network";
import { aws_ec2 as ec2, App, Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";

export class VPCStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps = {}) {
    const s3EndpointIamPermission = new iam.PolicyStatement({
      actions: ["s3:*"],
      resources: ['arn:aws:s3:::*'],
      principals: [new iam.AnyPrincipal()],
    })
    const monitoringEndpointIamPermission = new iam.PolicyStatement({
      actions: ["*"],
      resources: ['*'],
      principals: [new iam.AnyPrincipal()],
    })
    super(scope, id, props);
    new Network(this, 'NETWORK', {
      vpc: {
        cidr: '10.10.0.0/16',
        subnetConfiguration: [],
      },
      peeringConfigs: {
        "TEST-PEERING": { // this key will be used as your peering id, which you will have to mention below when you configure a route table for your subnets
          peeringVpcId: "vpc-0000",
          tags: {
            "Name": "TEST-PEERING to CREATED-VPC",
            "Description": "Connect"
          }
        }
      },
      subnets: [
        {
          subnetGroupName: 'NATGateway',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrBlock: ['10.10.0.0/28', '10.10.0.16/28', '10.10.0.32/28'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
        },
        {
          subnetGroupName: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrBlock: ['10.10.2.0/24', '10.10.3.0/24', '10.10.4.0/24'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          tags: {
            // if you use this vpc for your eks cluster, you have to tag your subnets [read more](https://aws.amazon.com/premiumsupport/knowledge-center/eks-vpc-subnet-discovery/)
            'kubernetes.io/role/elb': '1',
            'kubernetes.io/cluster/TEST-CLUSTER': 'owned',
          },
        },
        {
          subnetGroupName: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrBlock: ['10.10.5.0/24', '10.10.6.0/24', '10.10.7.0/24'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },

          ],
          routes: [
            {
            // if you use this vpc for your eks cluster, you have to tag your subnets [read more](https://aws.amazon.com/premiumsupport/knowledge-center/eks-vpc-subnet-discovery/)
              routerType: ec2.RouterType.VPC_PEERING_CONNECTION,
              destinationCidrBlock: "<destinationCidrBlock>",
              //<Your VPC PeeringConfig KEY, in this example TEST-PEERING will be your ID>
              existingVpcPeeringRouteKey: "TEST-PEERING"
            }
          ],
          tags: {
            'kubernetes.io/role/internal-elb': '1',
            'kubernetes.io/cluster/TEST-CLUSTER': 'owned',
          },
        },
        {
          subnetGroupName: 'Database',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrBlock: ['10.10.14.0/27', '10.10.14.32/27', '10.10.14.64/27'],
          availabilityZones: ['ap-south-1a', 'ap-south-1b', 'ap-south-1c'],
          ingressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          egressNetworkACL: [
            {
              cidr: ec2.AclCidr.ipv4('0.0.0.0/0'),
              traffic: ec2.AclTraffic.allTraffic(),
            },
          ],
          routes: [
          ],
          tags: {
          },
        },
      ],
      vpcEndpoints: [
        {
          name: "s3-gw",
          service: ec2.GatewayVpcEndpointAwsService.S3,
          subnetGroupNames: ["Private","Database"],
          externalSubnets: [
            {
              id: "subnet-<id>",
              availabilityZone: "ap-south-1a",
              routeTableId: "rtb-<id>"
            },
            {
              id: "subnet-<id>",
              availabilityZone: "ap-south-1b",
              routeTableId: "rtb-<id>"
            }
          ],
          iamPolicyStatements: [s3EndpointIamPermission]
        },
        {
          name: "da-stag-monitoring-vpe",
          service: ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_MONITORING,
          subnetGroupNames: ["ManageServicePrivate"],
          iamPolicyStatements: [monitoringEndpointIamPermission],
          securityGroupRules: [
            {
              peer: ec2.Peer.ipv4("10.10.0.0/16"),
              port:  ec2.Port.tcp(443),
              description: "From Test VPC"
            }
          ],
        },
      ]
    });
  }
}
const envDef = {
  account: '<AWS-ID>',
  region: '<AWS-REGION>',
};

const app = new App();

new VPCStack(app, 'TEST', {
  env: envDef,
  terminationProtection: true,
  tags: {
});
app.synth();
```

Please refer [here](/API.md) to check how to use individual resource constructs.

## :clapper: Quick Start

The quick start shows you how to create an **AWS-VPC** using this module.

### Prerequisites

* A working [`aws`](https://aws.amazon.com/cli/) CLI installation with access to an account and administrator privileges
* You'll need a recent [NodeJS](https://nodejs.org) installation

To get going you'll need a CDK project. For details please refer to the [detailed guide for CDK](https://docs.aws.amazon.com/cdk/latest/guide/hello_world.html).

Create an empty directory on your system.

```bash
mkdir aws-quick-start-vpc && cd aws-quick-start-vpc
```

Bootstrap your CDK project, we will use TypeScript, but you can switch to any other supported language.

```bash
npx cdk init sample-vpc  --language typescript
npx cdk bootstrap
```

Install using NPM:

```
npm install @smallcase/cdk-vpc-module
```

Using yarn

```
yarn add @smallcase/cdk-vpc-module
```

Check the changed which are to be deployed

```bash
~ -> npx cdk diff
```

Deploy using

```bash
~ -> npx cdk deploy
```

Features
Multiple VPC Endpoints: Define and manage multiple VPC Endpoints in one configuration.
Flexible Subnet Selection: Attach VPC Endpoints to multiple subnet groups or external subnets.
Custom Security Groups: Configure security groups for Interface VPC Endpoints.
IAM Policies: Attach custom IAM policies to control access to the VPC Endpoints.
Tagging: Apply custom tags to each VPC Endpoint.

Defining VPC Endpoints Configuration
You can define multiple VPC Endpoints in the vpcEndpoints: [] configuration array. Each VPC Endpoint can be customized with different subnet groups, IAM policies, security group rules, and tags.

```
vpcEndpoints: [
  {
    name: "test-s3-gw",
    service: ec2.GatewayVpcEndpointAwsService.S3,
    subnetGroupNames: ["ManageServicePrivate", "ToolPrivate", "Database"],  // Subnet groups for the endpoint
    externalSubnets: [
      {
        id: "subnet-<id>",
        availabilityZone: "ap-south-1a",
        routeTableId: "rtb-<id>",
      },
      {
        id: "subnet-<id>",
        availabilityZone: "ap-south-1b",
        routeTableId: "rtb-<id>",
      }
    ],
    iamPolicyStatements: [s3EndpointIamPermission],  // Custom IAM policy for the endpoint
  },
  {
    name: "DynamoDbGatewayEndpoint",
    service: ec2.GatewayVpcEndpointAwsService.DYNAMODB,
    subnetGroupNames: ["private-subnet"],
    additionalTags: {
      Environment: "Staging",
    },
  },
],
```

In this example:

The S3 Gateway Endpoint is created in three subnet groups: ManageServicePrivate, ToolPrivate, and Database.
External subnets are specified with their IDs, availability zones, and route table IDs for the S3 endpoint.
A custom IAM policy (s3EndpointIamPermission) is attached to control access to the S3 endpoint.
A DynamoDB Gateway Endpoint is created in the private-subnet with additional tags specifying the environment and ownership.

Configuration Options
Here’s a breakdown of the configuration options available:

1. name: A unique name for the VPC Endpoint.
2. service: The AWS service the VPC Endpoint connects to (e.g., S3, DynamoDB, Secrets Manager)
3. subnetGroupNames: The subnet group names where the VPC Endpoint will be deployed.
4. externalSubnets: Specify external subnets if you need to define subnets manually (each with an id, availabilityZone, and routeTableId).
5. iamPolicyStatements: (Optional) Attach IAM policy statements to control access to the endpoint.
6. additionalTags: (Optional) Add custom tags to the VPC Endpoint for easier identification and tracking.

* :white_check_mark: Configurable route table entry naming for subnet routes via `routeTableStringFormat`
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.AddRouteOptions",
    jsii_struct_bases=[],
    name_mapping={
        "router_type": "routerType",
        "destination_cidr_block": "destinationCidrBlock",
        "destination_ipv6_cidr_block": "destinationIpv6CidrBlock",
        "enables_internet_connectivity": "enablesInternetConnectivity",
        "existing_vpc_peering_route_key": "existingVpcPeeringRouteKey",
        "route_name": "routeName",
        "router_id": "routerId",
    },
)
class AddRouteOptions:
    def __init__(
        self,
        *,
        router_type: _aws_cdk_aws_ec2_ceddda9d.RouterType,
        destination_cidr_block: typing.Optional[builtins.str] = None,
        destination_ipv6_cidr_block: typing.Optional[builtins.str] = None,
        enables_internet_connectivity: typing.Optional[builtins.bool] = None,
        existing_vpc_peering_route_key: typing.Optional[builtins.str] = None,
        route_name: typing.Optional[builtins.str] = None,
        router_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param router_type: What type of router to route this traffic to.
        :param destination_cidr_block: IPv4 range this route applies to. Default: '0.0.0.0/0'
        :param destination_ipv6_cidr_block: IPv6 range this route applies to. Default: - Uses IPv6
        :param enables_internet_connectivity: Whether this route will enable internet connectivity. If true, this route will be added before any AWS resources that depend on internet connectivity in the VPC will be created. Default: false
        :param existing_vpc_peering_route_key: 
        :param route_name: 
        :param router_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77cff1a961dfe56849028f489d387bf7a42f4363289b43e3bab5a7a69aec3aa6)
            check_type(argname="argument router_type", value=router_type, expected_type=type_hints["router_type"])
            check_type(argname="argument destination_cidr_block", value=destination_cidr_block, expected_type=type_hints["destination_cidr_block"])
            check_type(argname="argument destination_ipv6_cidr_block", value=destination_ipv6_cidr_block, expected_type=type_hints["destination_ipv6_cidr_block"])
            check_type(argname="argument enables_internet_connectivity", value=enables_internet_connectivity, expected_type=type_hints["enables_internet_connectivity"])
            check_type(argname="argument existing_vpc_peering_route_key", value=existing_vpc_peering_route_key, expected_type=type_hints["existing_vpc_peering_route_key"])
            check_type(argname="argument route_name", value=route_name, expected_type=type_hints["route_name"])
            check_type(argname="argument router_id", value=router_id, expected_type=type_hints["router_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "router_type": router_type,
        }
        if destination_cidr_block is not None:
            self._values["destination_cidr_block"] = destination_cidr_block
        if destination_ipv6_cidr_block is not None:
            self._values["destination_ipv6_cidr_block"] = destination_ipv6_cidr_block
        if enables_internet_connectivity is not None:
            self._values["enables_internet_connectivity"] = enables_internet_connectivity
        if existing_vpc_peering_route_key is not None:
            self._values["existing_vpc_peering_route_key"] = existing_vpc_peering_route_key
        if route_name is not None:
            self._values["route_name"] = route_name
        if router_id is not None:
            self._values["router_id"] = router_id

    @builtins.property
    def router_type(self) -> _aws_cdk_aws_ec2_ceddda9d.RouterType:
        '''What type of router to route this traffic to.'''
        result = self._values.get("router_type")
        assert result is not None, "Required property 'router_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.RouterType, result)

    @builtins.property
    def destination_cidr_block(self) -> typing.Optional[builtins.str]:
        '''IPv4 range this route applies to.

        :default: '0.0.0.0/0'
        '''
        result = self._values.get("destination_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_ipv6_cidr_block(self) -> typing.Optional[builtins.str]:
        '''IPv6 range this route applies to.

        :default: - Uses IPv6
        '''
        result = self._values.get("destination_ipv6_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enables_internet_connectivity(self) -> typing.Optional[builtins.bool]:
        '''Whether this route will enable internet connectivity.

        If true, this route will be added before any AWS resources that depend
        on internet connectivity in the VPC will be created.

        :default: false
        '''
        result = self._values.get("enables_internet_connectivity")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def existing_vpc_peering_route_key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("existing_vpc_peering_route_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("route_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("router_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddRouteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@smallcase/cdk-vpc-module.IExternalVPEndpointSubnets")
class IExternalVPEndpointSubnets(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> builtins.str:
        ...


class _IExternalVPEndpointSubnetsProxy:
    __jsii_type__: typing.ClassVar[str] = "@smallcase/cdk-vpc-module.IExternalVPEndpointSubnets"

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeTableId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IExternalVPEndpointSubnets).__jsii_proxy_class__ = lambda : _IExternalVPEndpointSubnetsProxy


@jsii.interface(jsii_type="@smallcase/cdk-vpc-module.ISubnetsProps")
class ISubnetsProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> typing.List[builtins.str]:
        ...

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        ...

    @builtins.property
    @jsii.member(jsii_name="egressNetworkACL")
    def egress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="ingressNetworkACL")
    def ingress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="routes")
    def routes(self) -> typing.Optional[typing.List[AddRouteOptions]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="routeTableStringFormat")
    def route_table_string_format(self) -> typing.Optional[builtins.bool]:
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        ...

    @builtins.property
    @jsii.member(jsii_name="useNestedStacks")
    def use_nested_stacks(self) -> typing.Optional[builtins.bool]:
        ...

    @builtins.property
    @jsii.member(jsii_name="useSubnetForNAT")
    def use_subnet_for_nat(self) -> typing.Optional[builtins.bool]:
        ...


class _ISubnetsPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@smallcase/cdk-vpc-module.ISubnetsProps"

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetGroupName"))

    @builtins.property
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetType:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetType, jsii.get(self, "subnetType"))

    @builtins.property
    @jsii.member(jsii_name="egressNetworkACL")
    def egress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        return typing.cast(typing.Optional[typing.List["NetworkACL"]], jsii.get(self, "egressNetworkACL"))

    @builtins.property
    @jsii.member(jsii_name="ingressNetworkACL")
    def ingress_network_acl(self) -> typing.Optional[typing.List["NetworkACL"]]:
        return typing.cast(typing.Optional[typing.List["NetworkACL"]], jsii.get(self, "ingressNetworkACL"))

    @builtins.property
    @jsii.member(jsii_name="routes")
    def routes(self) -> typing.Optional[typing.List[AddRouteOptions]]:
        return typing.cast(typing.Optional[typing.List[AddRouteOptions]], jsii.get(self, "routes"))

    @builtins.property
    @jsii.member(jsii_name="routeTableStringFormat")
    def route_table_string_format(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "routeTableStringFormat"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="useNestedStacks")
    def use_nested_stacks(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useNestedStacks"))

    @builtins.property
    @jsii.member(jsii_name="useSubnetForNAT")
    def use_subnet_for_nat(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useSubnetForNAT"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISubnetsProps).__jsii_proxy_class__ = lambda : _ISubnetsPropsProxy


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.LoadBalancerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "certificates": "certificates",
        "existing_arn": "existingArn",
        "existing_security_group_id": "existingSecurityGroupId",
        "internet_facing": "internetFacing",
        "security_group_rules": "securityGroupRules",
        "subnet_group_name": "subnetGroupName",
        "target_groups": "targetGroups",
    },
)
class LoadBalancerConfig:
    def __init__(
        self,
        *,
        certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        existing_arn: typing.Optional[builtins.str] = None,
        existing_security_group_id: typing.Optional[builtins.str] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        security_group_rules: typing.Optional[typing.Sequence[typing.Union["SecurityGroupRule", typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        target_groups: typing.Optional[typing.Sequence[typing.Union["TargetGroupConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param certificates: 
        :param existing_arn: 
        :param existing_security_group_id: 
        :param internet_facing: 
        :param security_group_rules: 
        :param subnet_group_name: 
        :param target_groups: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294cecf3ca27764108cc34f1dcceaeb7af4089cca13b76c1182c89360fd852ba)
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument existing_arn", value=existing_arn, expected_type=type_hints["existing_arn"])
            check_type(argname="argument existing_security_group_id", value=existing_security_group_id, expected_type=type_hints["existing_security_group_id"])
            check_type(argname="argument internet_facing", value=internet_facing, expected_type=type_hints["internet_facing"])
            check_type(argname="argument security_group_rules", value=security_group_rules, expected_type=type_hints["security_group_rules"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificates is not None:
            self._values["certificates"] = certificates
        if existing_arn is not None:
            self._values["existing_arn"] = existing_arn
        if existing_security_group_id is not None:
            self._values["existing_security_group_id"] = existing_security_group_id
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if security_group_rules is not None:
            self._values["security_group_rules"] = security_group_rules
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if target_groups is not None:
            self._values["target_groups"] = target_groups

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def existing_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("existing_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def existing_security_group_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("existing_security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_group_rules(self) -> typing.Optional[typing.List["SecurityGroupRule"]]:
        result = self._values.get("security_group_rules")
        return typing.cast(typing.Optional[typing.List["SecurityGroupRule"]], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["TargetGroupConfig"]]:
        result = self._values.get("target_groups")
        return typing.cast(typing.Optional[typing.List["TargetGroupConfig"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Network(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-vpc-module.Network",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        subnets: typing.Sequence[ISubnetsProps],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
        nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union["PeeringConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
        use_nested_stacks: typing.Optional[builtins.bool] = None,
        vpc_endpoints: typing.Optional[typing.Sequence[typing.Union["VpcEndpointConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoint_services: typing.Optional[typing.Sequence[typing.Union["VpcEndpontServiceConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param subnets: 
        :param vpc: 
        :param nat_eip_allocation_ids: 
        :param peering_configs: 
        :param use_nested_stacks: 
        :param vpc_endpoints: 
        :param vpc_endpoint_services: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3f88ed1cc891dbd636f210624927d010c33ac961e6f577806e2dd937c456be)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VPCProps(
            subnets=subnets,
            vpc=vpc,
            nat_eip_allocation_ids=nat_eip_allocation_ids,
            peering_configs=peering_configs,
            use_nested_stacks=use_nested_stacks,
            vpc_endpoints=vpc_endpoints,
            vpc_endpoint_services=vpc_endpoint_services,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createSubnet")
    def create_subnet(
        self,
        option: ISubnetsProps,
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
        peering_connection_id: typing.Optional[typing.Union["PeeringConnectionInternalType", typing.Dict[builtins.str, typing.Any]]] = None,
        use_global_nested_stacks: typing.Optional[builtins.bool] = None,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]:
        '''
        :param option: -
        :param vpc: -
        :param peering_connection_id: -
        :param use_global_nested_stacks: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92666cd41c2c14d24ac75176f78720cccdba04127eb90a149be6f2fe21660cf1)
            check_type(argname="argument option", value=option, expected_type=type_hints["option"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument peering_connection_id", value=peering_connection_id, expected_type=type_hints["peering_connection_id"])
            check_type(argname="argument use_global_nested_stacks", value=use_global_nested_stacks, expected_type=type_hints["use_global_nested_stacks"])
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet], jsii.invoke(self, "createSubnet", [option, vpc, peering_connection_id, use_global_nested_stacks]))

    @builtins.property
    @jsii.member(jsii_name="endpointOutputs")
    def endpoint_outputs(
        self,
    ) -> typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpoint, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpoint]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpoint, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpoint]], jsii.get(self, "endpointOutputs"))

    @builtins.property
    @jsii.member(jsii_name="natProvider")
    def nat_provider(self) -> _aws_cdk_aws_ec2_ceddda9d.NatProvider:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.NatProvider, jsii.get(self, "natProvider"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupOutputs")
    def security_group_outputs(
        self,
    ) -> typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.SecurityGroup]:
        return typing.cast(typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.SecurityGroup], jsii.get(self, "securityGroupOutputs"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.Vpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="natSubnets")
    def nat_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet], jsii.get(self, "natSubnets"))

    @nat_subnets.setter
    def nat_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78b8adef4396361d5c72de5dc0fba4922e4d9a7322c65f75ff8504d4bd76871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "natSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pbSubnets")
    def pb_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet], jsii.get(self, "pbSubnets"))

    @pb_subnets.setter
    def pb_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69712fe7b2bc40ff22d1946b13d47d502e7bdb75a27de5e82a782f5b1e5ad06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pbSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pvSubnets")
    def pv_subnets(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet]:
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet], jsii.get(self, "pvSubnets"))

    @pv_subnets.setter
    def pv_subnets(
        self,
        value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bfb10a99897571241006d792ce84acf324e915d0d0d7a70310260bbf97506a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pvSubnets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(
        self,
    ) -> typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]]:
        return typing.cast(typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]], jsii.get(self, "subnets"))

    @subnets.setter
    def subnets(
        self,
        value: typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1c92e4cdb3e7dca57b71939ecd52b3318b82f9250bdbeca196ba690ca35f52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnets", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.NetworkACL",
    jsii_struct_bases=[],
    name_mapping={"cidr": "cidr", "traffic": "traffic"},
)
class NetworkACL:
    def __init__(
        self,
        *,
        cidr: _aws_cdk_aws_ec2_ceddda9d.AclCidr,
        traffic: _aws_cdk_aws_ec2_ceddda9d.AclTraffic,
    ) -> None:
        '''
        :param cidr: 
        :param traffic: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1970396c779835fc4afcade9ad3fdc707402f18a94acc262cf9e711955157f)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument traffic", value=traffic, expected_type=type_hints["traffic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
            "traffic": traffic,
        }

    @builtins.property
    def cidr(self) -> _aws_cdk_aws_ec2_ceddda9d.AclCidr:
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.AclCidr, result)

    @builtins.property
    def traffic(self) -> _aws_cdk_aws_ec2_ceddda9d.AclTraffic:
        result = self._values.get("traffic")
        assert result is not None, "Required property 'traffic' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.AclTraffic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkACL(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.NetworkLoadBalancerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_rules": "securityGroupRules",
        "subnet_group_name": "subnetGroupName",
        "certificates": "certificates",
        "existing_security_group_id": "existingSecurityGroupId",
        "internet_facing": "internetFacing",
    },
)
class NetworkLoadBalancerConfig:
    def __init__(
        self,
        *,
        security_group_rules: typing.Sequence[typing.Union["SecurityGroupRule", typing.Dict[builtins.str, typing.Any]]],
        subnet_group_name: builtins.str,
        certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
        existing_security_group_id: typing.Optional[builtins.str] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param security_group_rules: 
        :param subnet_group_name: 
        :param certificates: 
        :param existing_security_group_id: 
        :param internet_facing: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a56ad2276471c8487497d46d652ec1744988a1cc4eb2d45c5e49265e3395d0)
            check_type(argname="argument security_group_rules", value=security_group_rules, expected_type=type_hints["security_group_rules"])
            check_type(argname="argument subnet_group_name", value=subnet_group_name, expected_type=type_hints["subnet_group_name"])
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument existing_security_group_id", value=existing_security_group_id, expected_type=type_hints["existing_security_group_id"])
            check_type(argname="argument internet_facing", value=internet_facing, expected_type=type_hints["internet_facing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "security_group_rules": security_group_rules,
            "subnet_group_name": subnet_group_name,
        }
        if certificates is not None:
            self._values["certificates"] = certificates
        if existing_security_group_id is not None:
            self._values["existing_security_group_id"] = existing_security_group_id
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing

    @builtins.property
    def security_group_rules(self) -> typing.List["SecurityGroupRule"]:
        result = self._values.get("security_group_rules")
        assert result is not None, "Required property 'security_group_rules' is missing"
        return typing.cast(typing.List["SecurityGroupRule"], result)

    @builtins.property
    def subnet_group_name(self) -> builtins.str:
        result = self._values.get("subnet_group_name")
        assert result is not None, "Required property 'subnet_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificates(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def existing_security_group_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("existing_security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkLoadBalancerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.PeeringConfig",
    jsii_struct_bases=[],
    name_mapping={
        "peering_vpc_id": "peeringVpcId",
        "tags": "tags",
        "peer_assume_role_arn": "peerAssumeRoleArn",
        "peer_owner_id": "peerOwnerId",
        "peer_region": "peerRegion",
    },
)
class PeeringConfig:
    def __init__(
        self,
        *,
        peering_vpc_id: builtins.str,
        tags: typing.Mapping[builtins.str, builtins.str],
        peer_assume_role_arn: typing.Optional[builtins.str] = None,
        peer_owner_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param peering_vpc_id: 
        :param tags: 
        :param peer_assume_role_arn: 
        :param peer_owner_id: 
        :param peer_region: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906788234b850289efe7c3dfd41ad9a7598ad048a1820338c1962e640c00d246)
            check_type(argname="argument peering_vpc_id", value=peering_vpc_id, expected_type=type_hints["peering_vpc_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument peer_assume_role_arn", value=peer_assume_role_arn, expected_type=type_hints["peer_assume_role_arn"])
            check_type(argname="argument peer_owner_id", value=peer_owner_id, expected_type=type_hints["peer_owner_id"])
            check_type(argname="argument peer_region", value=peer_region, expected_type=type_hints["peer_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peering_vpc_id": peering_vpc_id,
            "tags": tags,
        }
        if peer_assume_role_arn is not None:
            self._values["peer_assume_role_arn"] = peer_assume_role_arn
        if peer_owner_id is not None:
            self._values["peer_owner_id"] = peer_owner_id
        if peer_region is not None:
            self._values["peer_region"] = peer_region

    @builtins.property
    def peering_vpc_id(self) -> builtins.str:
        result = self._values.get("peering_vpc_id")
        assert result is not None, "Required property 'peering_vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def peer_assume_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_assume_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_owner_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_region(self) -> typing.Optional[builtins.str]:
        result = self._values.get("peer_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeeringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.PeeringConnectionInternalType",
    jsii_struct_bases=[],
    name_mapping={},
)
class PeeringConnectionInternalType:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PeeringConnectionInternalType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.SecurityGroupRule",
    jsii_struct_bases=[],
    name_mapping={"peer": "peer", "port": "port", "description": "description"},
)
class SecurityGroupRule:
    def __init__(
        self,
        *,
        peer: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IPeer, _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
        port: _aws_cdk_aws_ec2_ceddda9d.Port,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param peer: 
        :param port: 
        :param description: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd68ce1d83764f7d07cea64483e8a41653ce9918274f406bd230a98a95864f8a)
            check_type(argname="argument peer", value=peer, expected_type=type_hints["peer"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "peer": peer,
            "port": port,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def peer(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.IPeer, _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        result = self._values.get("peer")
        assert result is not None, "Required property 'peer' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.IPeer, _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def port(self) -> _aws_cdk_aws_ec2_ceddda9d.Port:
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Port, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityGroupRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.TargetGroupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "application_port": "applicationPort",
        "host": "host",
        "health_check_path": "healthCheckPath",
        "health_check_port": "healthCheckPort",
        "health_check_protocol": "healthCheckProtocol",
        "priority": "priority",
        "protocol": "protocol",
        "protocol_version": "protocolVersion",
    },
)
class TargetGroupConfig:
    def __init__(
        self,
        *,
        application_port: jsii.Number,
        host: builtins.str,
        health_check_path: typing.Optional[builtins.str] = None,
        health_check_port: typing.Optional[jsii.Number] = None,
        health_check_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.Protocol] = None,
        priority: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
        protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion] = None,
    ) -> None:
        '''
        :param application_port: 
        :param host: 
        :param health_check_path: 
        :param health_check_port: 
        :param health_check_protocol: 
        :param priority: 
        :param protocol: 
        :param protocol_version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48ede81cf9a8399dd6cd981152913c8750372d401f96aa406f65f559840bd034)
            check_type(argname="argument application_port", value=application_port, expected_type=type_hints["application_port"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument health_check_port", value=health_check_port, expected_type=type_hints["health_check_port"])
            check_type(argname="argument health_check_protocol", value=health_check_protocol, expected_type=type_hints["health_check_protocol"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_port": application_port,
            "host": host,
        }
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if health_check_port is not None:
            self._values["health_check_port"] = health_check_port
        if health_check_protocol is not None:
            self._values["health_check_protocol"] = health_check_protocol
        if priority is not None:
            self._values["priority"] = priority
        if protocol is not None:
            self._values["protocol"] = protocol
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version

    @builtins.property
    def application_port(self) -> jsii.Number:
        result = self._values.get("application_port")
        assert result is not None, "Required property 'application_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def host(self) -> builtins.str:
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_port(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("health_check_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.Protocol]:
        result = self._values.get("health_check_protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.Protocol], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol]:
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol], result)

    @builtins.property
    def protocol_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion]:
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.VPCProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnets": "subnets",
        "vpc": "vpc",
        "nat_eip_allocation_ids": "natEipAllocationIds",
        "peering_configs": "peeringConfigs",
        "use_nested_stacks": "useNestedStacks",
        "vpc_endpoints": "vpcEndpoints",
        "vpc_endpoint_services": "vpcEndpointServices",
    },
)
class VPCProps:
    def __init__(
        self,
        *,
        subnets: typing.Sequence[ISubnetsProps],
        vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
        nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union[PeeringConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
        use_nested_stacks: typing.Optional[builtins.bool] = None,
        vpc_endpoints: typing.Optional[typing.Sequence[typing.Union["VpcEndpointConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_endpoint_services: typing.Optional[typing.Sequence[typing.Union["VpcEndpontServiceConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param subnets: 
        :param vpc: 
        :param nat_eip_allocation_ids: 
        :param peering_configs: 
        :param use_nested_stacks: 
        :param vpc_endpoints: 
        :param vpc_endpoint_services: 
        '''
        if isinstance(vpc, dict):
            vpc = _aws_cdk_aws_ec2_ceddda9d.VpcProps(**vpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__276e14ede93619c8496d33625e8b9426df9db19c536b76f6785db1fff0434a40)
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument nat_eip_allocation_ids", value=nat_eip_allocation_ids, expected_type=type_hints["nat_eip_allocation_ids"])
            check_type(argname="argument peering_configs", value=peering_configs, expected_type=type_hints["peering_configs"])
            check_type(argname="argument use_nested_stacks", value=use_nested_stacks, expected_type=type_hints["use_nested_stacks"])
            check_type(argname="argument vpc_endpoints", value=vpc_endpoints, expected_type=type_hints["vpc_endpoints"])
            check_type(argname="argument vpc_endpoint_services", value=vpc_endpoint_services, expected_type=type_hints["vpc_endpoint_services"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnets": subnets,
            "vpc": vpc,
        }
        if nat_eip_allocation_ids is not None:
            self._values["nat_eip_allocation_ids"] = nat_eip_allocation_ids
        if peering_configs is not None:
            self._values["peering_configs"] = peering_configs
        if use_nested_stacks is not None:
            self._values["use_nested_stacks"] = use_nested_stacks
        if vpc_endpoints is not None:
            self._values["vpc_endpoints"] = vpc_endpoints
        if vpc_endpoint_services is not None:
            self._values["vpc_endpoint_services"] = vpc_endpoint_services

    @builtins.property
    def subnets(self) -> typing.List[ISubnetsProps]:
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[ISubnetsProps], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.VpcProps:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.VpcProps, result)

    @builtins.property
    def nat_eip_allocation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("nat_eip_allocation_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def peering_configs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, PeeringConfig]]:
        result = self._values.get("peering_configs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, PeeringConfig]], result)

    @builtins.property
    def use_nested_stacks(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("use_nested_stacks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_endpoints(self) -> typing.Optional[typing.List["VpcEndpointConfig"]]:
        result = self._values.get("vpc_endpoints")
        return typing.cast(typing.Optional[typing.List["VpcEndpointConfig"]], result)

    @builtins.property
    def vpc_endpoint_services(
        self,
    ) -> typing.Optional[typing.List["VpcEndpontServiceConfig"]]:
        result = self._values.get("vpc_endpoint_services")
        return typing.cast(typing.Optional[typing.List["VpcEndpontServiceConfig"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VPCProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.VpcEndpointConfig",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "service": "service",
        "subnet_group_names": "subnetGroupNames",
        "additional_tags": "additionalTags",
        "external_subnets": "externalSubnets",
        "iam_policy_statements": "iamPolicyStatements",
        "security_group_rules": "securityGroupRules",
    },
)
class VpcEndpointConfig:
    def __init__(
        self,
        *,
        name: builtins.str,
        service: typing.Union[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointService],
        subnet_group_names: typing.Sequence[builtins.str],
        additional_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        external_subnets: typing.Optional[typing.Sequence[IExternalVPEndpointSubnets]] = None,
        iam_policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        security_group_rules: typing.Optional[typing.Sequence[typing.Union[SecurityGroupRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param name: 
        :param service: 
        :param subnet_group_names: 
        :param additional_tags: 
        :param external_subnets: 
        :param iam_policy_statements: 
        :param security_group_rules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73b977d0ef95f1e08b08f9303890f3ab452756f6c151eea2ffe6c531ffe2ecc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument subnet_group_names", value=subnet_group_names, expected_type=type_hints["subnet_group_names"])
            check_type(argname="argument additional_tags", value=additional_tags, expected_type=type_hints["additional_tags"])
            check_type(argname="argument external_subnets", value=external_subnets, expected_type=type_hints["external_subnets"])
            check_type(argname="argument iam_policy_statements", value=iam_policy_statements, expected_type=type_hints["iam_policy_statements"])
            check_type(argname="argument security_group_rules", value=security_group_rules, expected_type=type_hints["security_group_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "service": service,
            "subnet_group_names": subnet_group_names,
        }
        if additional_tags is not None:
            self._values["additional_tags"] = additional_tags
        if external_subnets is not None:
            self._values["external_subnets"] = external_subnets
        if iam_policy_statements is not None:
            self._values["iam_policy_statements"] = iam_policy_statements
        if security_group_rules is not None:
            self._values["security_group_rules"] = security_group_rules

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(
        self,
    ) -> typing.Union[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointService]:
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(typing.Union[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointService], result)

    @builtins.property
    def subnet_group_names(self) -> typing.List[builtins.str]:
        result = self._values.get("subnet_group_names")
        assert result is not None, "Required property 'subnet_group_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def additional_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("additional_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def external_subnets(
        self,
    ) -> typing.Optional[typing.List[IExternalVPEndpointSubnets]]:
        result = self._values.get("external_subnets")
        return typing.cast(typing.Optional[typing.List[IExternalVPEndpointSubnets]], result)

    @builtins.property
    def iam_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        result = self._values.get("iam_policy_statements")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], result)

    @builtins.property
    def security_group_rules(self) -> typing.Optional[typing.List[SecurityGroupRule]]:
        result = self._values.get("security_group_rules")
        return typing.cast(typing.Optional[typing.List[SecurityGroupRule]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcEndpointServiceNestedStack(
    _aws_cdk_ceddda9d.NestedStack,
    metaclass=jsii.JSIIMeta,
    jsii_type="@smallcase/cdk-vpc-module.VpcEndpointServiceNestedStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        subnets: typing.Mapping[builtins.str, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Subnet]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
        vpc_endpoint_service_configs: typing.Sequence[typing.Union["VpcEndpontServiceConfig", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param subnets: 
        :param vpc: 
        :param vpc_endpoint_service_configs: 
        :param description: A description of the stack. Default: - No description.
        :param notification_arns: The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param removal_policy: Policy to apply when the nested stack is removed. The default is ``Destroy``, because all Removal Policies of resources inside the Nested Stack should already have been set correctly. You normally should not need to set this value. Default: RemovalPolicy.DESTROY
        :param timeout: The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26df69a42e4412f21ea0edc5da55f7bd41d69c8c97dba4ec21c6dc94fb72828)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpcEndpointServiceNestedStackProps(
            subnets=subnets,
            vpc=vpc,
            vpc_endpoint_service_configs=vpc_endpoint_service_configs,
            description=description,
            notification_arns=notification_arns,
            parameters=parameters,
            removal_policy=removal_policy,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.VpcEndpointServiceNestedStackProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.NestedStackProps],
    name_mapping={
        "description": "description",
        "notification_arns": "notificationArns",
        "parameters": "parameters",
        "removal_policy": "removalPolicy",
        "timeout": "timeout",
        "subnets": "subnets",
        "vpc": "vpc",
        "vpc_endpoint_service_configs": "vpcEndpointServiceConfigs",
    },
)
class VpcEndpointServiceNestedStackProps(_aws_cdk_ceddda9d.NestedStackProps):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        subnets: typing.Mapping[builtins.str, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Subnet]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
        vpc_endpoint_service_configs: typing.Sequence[typing.Union["VpcEndpontServiceConfig", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param description: A description of the stack. Default: - No description.
        :param notification_arns: The Simple Notification Service (SNS) topics to publish stack related events. Default: - notifications are not sent for this stack.
        :param parameters: The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created. Each parameter has a name corresponding to a parameter defined in the embedded template and a value representing the value that you want to set for the parameter. The nested stack construct will automatically synthesize parameters in order to bind references from the parent stack(s) into the nested stack. Default: - no user-defined parameters are passed to the nested stack
        :param removal_policy: Policy to apply when the nested stack is removed. The default is ``Destroy``, because all Removal Policies of resources inside the Nested Stack should already have been set correctly. You normally should not need to set this value. Default: RemovalPolicy.DESTROY
        :param timeout: The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state. When CloudFormation detects that the nested stack has reached the CREATE_COMPLETE state, it marks the nested stack resource as CREATE_COMPLETE in the parent stack and resumes creating the parent stack. If the timeout period expires before the nested stack reaches CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls back both the nested stack and parent stack. Default: - no timeout
        :param subnets: 
        :param vpc: 
        :param vpc_endpoint_service_configs: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe2894760562a5d57899a47f1a777186cd677070f2d28f3a680fbc121af8e3f)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_endpoint_service_configs", value=vpc_endpoint_service_configs, expected_type=type_hints["vpc_endpoint_service_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnets": subnets,
            "vpc": vpc,
            "vpc_endpoint_service_configs": vpc_endpoint_service_configs,
        }
        if description is not None:
            self._values["description"] = description
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if parameters is not None:
            self._values["parameters"] = parameters
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Simple Notification Service (SNS) topics to publish stack related events.

        :default: - notifications are not sent for this stack.
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The set value pairs that represent the parameters passed to CloudFormation when this nested stack is created.

        Each parameter has a name corresponding
        to a parameter defined in the embedded template and a value representing
        the value that you want to set for the parameter.

        The nested stack construct will automatically synthesize parameters in order
        to bind references from the parent stack(s) into the nested stack.

        :default: - no user-defined parameters are passed to the nested stack
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Policy to apply when the nested stack is removed.

        The default is ``Destroy``, because all Removal Policies of resources inside the
        Nested Stack should already have been set correctly. You normally should
        not need to set this value.

        :default: RemovalPolicy.DESTROY
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The length of time that CloudFormation waits for the nested stack to reach the CREATE_COMPLETE state.

        When CloudFormation detects that the nested stack has reached the
        CREATE_COMPLETE state, it marks the nested stack resource as
        CREATE_COMPLETE in the parent stack and resumes creating the parent stack.
        If the timeout period expires before the nested stack reaches
        CREATE_COMPLETE, CloudFormation marks the nested stack as failed and rolls
        back both the nested stack and parent stack.

        :default: - no timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def subnets(
        self,
    ) -> typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]]:
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.Vpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, result)

    @builtins.property
    def vpc_endpoint_service_configs(self) -> typing.List["VpcEndpontServiceConfig"]:
        result = self._values.get("vpc_endpoint_service_configs")
        assert result is not None, "Required property 'vpc_endpoint_service_configs' is missing"
        return typing.cast(typing.List["VpcEndpontServiceConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEndpointServiceNestedStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@smallcase/cdk-vpc-module.VpcEndpontServiceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alb": "alb",
        "name": "name",
        "nlb": "nlb",
        "acceptance_required": "acceptanceRequired",
        "additional_tags": "additionalTags",
        "allowed_principals": "allowedPrincipals",
    },
)
class VpcEndpontServiceConfig:
    def __init__(
        self,
        *,
        alb: typing.Union[LoadBalancerConfig, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        nlb: typing.Union[NetworkLoadBalancerConfig, typing.Dict[builtins.str, typing.Any]],
        acceptance_required: typing.Optional[builtins.bool] = None,
        additional_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allowed_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param alb: 
        :param name: 
        :param nlb: 
        :param acceptance_required: 
        :param additional_tags: 
        :param allowed_principals: 
        '''
        if isinstance(alb, dict):
            alb = LoadBalancerConfig(**alb)
        if isinstance(nlb, dict):
            nlb = NetworkLoadBalancerConfig(**nlb)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7971811dc382b00c546c83de42175abd890c255c039e9ec4496f8b6b17c8475f)
            check_type(argname="argument alb", value=alb, expected_type=type_hints["alb"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nlb", value=nlb, expected_type=type_hints["nlb"])
            check_type(argname="argument acceptance_required", value=acceptance_required, expected_type=type_hints["acceptance_required"])
            check_type(argname="argument additional_tags", value=additional_tags, expected_type=type_hints["additional_tags"])
            check_type(argname="argument allowed_principals", value=allowed_principals, expected_type=type_hints["allowed_principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alb": alb,
            "name": name,
            "nlb": nlb,
        }
        if acceptance_required is not None:
            self._values["acceptance_required"] = acceptance_required
        if additional_tags is not None:
            self._values["additional_tags"] = additional_tags
        if allowed_principals is not None:
            self._values["allowed_principals"] = allowed_principals

    @builtins.property
    def alb(self) -> LoadBalancerConfig:
        result = self._values.get("alb")
        assert result is not None, "Required property 'alb' is missing"
        return typing.cast(LoadBalancerConfig, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nlb(self) -> NetworkLoadBalancerConfig:
        result = self._values.get("nlb")
        assert result is not None, "Required property 'nlb' is missing"
        return typing.cast(NetworkLoadBalancerConfig, result)

    @builtins.property
    def acceptance_required(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("acceptance_required")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def additional_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("additional_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def allowed_principals(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("allowed_principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcEndpontServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddRouteOptions",
    "IExternalVPEndpointSubnets",
    "ISubnetsProps",
    "LoadBalancerConfig",
    "Network",
    "NetworkACL",
    "NetworkLoadBalancerConfig",
    "PeeringConfig",
    "PeeringConnectionInternalType",
    "SecurityGroupRule",
    "TargetGroupConfig",
    "VPCProps",
    "VpcEndpointConfig",
    "VpcEndpointServiceNestedStack",
    "VpcEndpointServiceNestedStackProps",
    "VpcEndpontServiceConfig",
]

publication.publish()

def _typecheckingstub__77cff1a961dfe56849028f489d387bf7a42f4363289b43e3bab5a7a69aec3aa6(
    *,
    router_type: _aws_cdk_aws_ec2_ceddda9d.RouterType,
    destination_cidr_block: typing.Optional[builtins.str] = None,
    destination_ipv6_cidr_block: typing.Optional[builtins.str] = None,
    enables_internet_connectivity: typing.Optional[builtins.bool] = None,
    existing_vpc_peering_route_key: typing.Optional[builtins.str] = None,
    route_name: typing.Optional[builtins.str] = None,
    router_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294cecf3ca27764108cc34f1dcceaeb7af4089cca13b76c1182c89360fd852ba(
    *,
    certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    existing_arn: typing.Optional[builtins.str] = None,
    existing_security_group_id: typing.Optional[builtins.str] = None,
    internet_facing: typing.Optional[builtins.bool] = None,
    security_group_rules: typing.Optional[typing.Sequence[typing.Union[SecurityGroupRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_group_name: typing.Optional[builtins.str] = None,
    target_groups: typing.Optional[typing.Sequence[typing.Union[TargetGroupConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3f88ed1cc891dbd636f210624927d010c33ac961e6f577806e2dd937c456be(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    subnets: typing.Sequence[ISubnetsProps],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
    nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union[PeeringConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_nested_stacks: typing.Optional[builtins.bool] = None,
    vpc_endpoints: typing.Optional[typing.Sequence[typing.Union[VpcEndpointConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_services: typing.Optional[typing.Sequence[typing.Union[VpcEndpontServiceConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92666cd41c2c14d24ac75176f78720cccdba04127eb90a149be6f2fe21660cf1(
    option: ISubnetsProps,
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    peering_connection_id: typing.Optional[typing.Union[PeeringConnectionInternalType, typing.Dict[builtins.str, typing.Any]]] = None,
    use_global_nested_stacks: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78b8adef4396361d5c72de5dc0fba4922e4d9a7322c65f75ff8504d4bd76871(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69712fe7b2bc40ff22d1946b13d47d502e7bdb75a27de5e82a782f5b1e5ad06(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bfb10a99897571241006d792ce84acf324e915d0d0d7a70310260bbf97506a(
    value: typing.List[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c92e4cdb3e7dca57b71939ecd52b3318b82f9250bdbeca196ba690ca35f52(
    value: typing.Mapping[builtins.str, typing.List[_aws_cdk_aws_ec2_ceddda9d.Subnet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1970396c779835fc4afcade9ad3fdc707402f18a94acc262cf9e711955157f(
    *,
    cidr: _aws_cdk_aws_ec2_ceddda9d.AclCidr,
    traffic: _aws_cdk_aws_ec2_ceddda9d.AclTraffic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a56ad2276471c8487497d46d652ec1744988a1cc4eb2d45c5e49265e3395d0(
    *,
    security_group_rules: typing.Sequence[typing.Union[SecurityGroupRule, typing.Dict[builtins.str, typing.Any]]],
    subnet_group_name: builtins.str,
    certificates: typing.Optional[typing.Sequence[builtins.str]] = None,
    existing_security_group_id: typing.Optional[builtins.str] = None,
    internet_facing: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906788234b850289efe7c3dfd41ad9a7598ad048a1820338c1962e640c00d246(
    *,
    peering_vpc_id: builtins.str,
    tags: typing.Mapping[builtins.str, builtins.str],
    peer_assume_role_arn: typing.Optional[builtins.str] = None,
    peer_owner_id: typing.Optional[builtins.str] = None,
    peer_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd68ce1d83764f7d07cea64483e8a41653ce9918274f406bd230a98a95864f8a(
    *,
    peer: typing.Union[_aws_cdk_aws_ec2_ceddda9d.IPeer, _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
    port: _aws_cdk_aws_ec2_ceddda9d.Port,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48ede81cf9a8399dd6cd981152913c8750372d401f96aa406f65f559840bd034(
    *,
    application_port: jsii.Number,
    host: builtins.str,
    health_check_path: typing.Optional[builtins.str] = None,
    health_check_port: typing.Optional[jsii.Number] = None,
    health_check_protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.Protocol] = None,
    priority: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    protocol_version: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocolVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__276e14ede93619c8496d33625e8b9426df9db19c536b76f6785db1fff0434a40(
    *,
    subnets: typing.Sequence[ISubnetsProps],
    vpc: typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpcProps, typing.Dict[builtins.str, typing.Any]],
    nat_eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    peering_configs: typing.Optional[typing.Mapping[builtins.str, typing.Union[PeeringConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    use_nested_stacks: typing.Optional[builtins.bool] = None,
    vpc_endpoints: typing.Optional[typing.Sequence[typing.Union[VpcEndpointConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_endpoint_services: typing.Optional[typing.Sequence[typing.Union[VpcEndpontServiceConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73b977d0ef95f1e08b08f9303890f3ab452756f6c151eea2ffe6c531ffe2ecc(
    *,
    name: builtins.str,
    service: typing.Union[_aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointAwsService, _aws_cdk_aws_ec2_ceddda9d.InterfaceVpcEndpointService],
    subnet_group_names: typing.Sequence[builtins.str],
    additional_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    external_subnets: typing.Optional[typing.Sequence[IExternalVPEndpointSubnets]] = None,
    iam_policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    security_group_rules: typing.Optional[typing.Sequence[typing.Union[SecurityGroupRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26df69a42e4412f21ea0edc5da55f7bd41d69c8c97dba4ec21c6dc94fb72828(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    subnets: typing.Mapping[builtins.str, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Subnet]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    vpc_endpoint_service_configs: typing.Sequence[typing.Union[VpcEndpontServiceConfig, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe2894760562a5d57899a47f1a777186cd677070f2d28f3a680fbc121af8e3f(
    *,
    description: typing.Optional[builtins.str] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    subnets: typing.Mapping[builtins.str, typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.Subnet]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    vpc_endpoint_service_configs: typing.Sequence[typing.Union[VpcEndpontServiceConfig, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7971811dc382b00c546c83de42175abd890c255c039e9ec4496f8b6b17c8475f(
    *,
    alb: typing.Union[LoadBalancerConfig, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    nlb: typing.Union[NetworkLoadBalancerConfig, typing.Dict[builtins.str, typing.Any]],
    acceptance_required: typing.Optional[builtins.bool] = None,
    additional_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    allowed_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
