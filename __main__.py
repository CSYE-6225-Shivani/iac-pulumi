import pulumi, os
import pulumi_aws as aws
from dotenv import load_dotenv

load_dotenv()

config = pulumi.Config("vpc")
cidr_block = config.require("cidr_block")

VPC_TAG_NAME = os.getenv("VPC_TAG_NAME")
IGW_TAG_NAME = os.getenv("IGW_TAG_NAME")
PUBLIC_RT_TAG_NAME = os.getenv("PUBLIC_RT_TAG_NAME")
PRIVATE_RT_TAG_NAME = os.getenv("PRIVATE_RT_TAG_NAME")

PUBLIC_SUBNETS = [os.getenv("PUBLIC_SUBNET1"), os.getenv("PUBLIC_SUBNET2"), os.getenv("PUBLIC_SUBNET3")]
PRIVATE_SUBNETS = [os.getenv("PRIVATE_SUBNET1"), os.getenv("PRIVATE_SUBNET2"), os.getenv("PRIVATE_SUBNET3")]
PUBLIC_RT_CIDR = os.getenv("PUBLIC_RT_CIDR")
available = aws.get_availability_zones(state="available")
public_subnets = []
private_subnets = []

myvpc = aws.ec2.Vpc("myvpc",
    cidr_block=cidr_block,
    tags={
        "Name": VPC_TAG_NAME,
    })

number_of_az = len(available.names)

if number_of_az >= 3:
    for i in range(3):
        public_subnet = aws.ec2.Subnet(f"public-subnet-{i}",
                                   availability_zone=available.names[i],
                                   cidr_block=PUBLIC_SUBNETS[i],
                                   map_public_ip_on_launch=True,
                                   vpc_id=myvpc.id)
        private_subnet = aws.ec2.Subnet(f"private-subnet-{i}",
                                    availability_zone=available.names[i],
                                    cidr_block=PRIVATE_SUBNETS[i],
                                    map_public_ip_on_launch=False,
                                    vpc_id=myvpc.id)
        public_subnets.append(public_subnet)
        private_subnets.append(private_subnet)
else:
    for i in range(number_of_az):
        public_subnet = aws.ec2.Subnet(f"public-subnet-{i}",
                                    availability_zone=available.names[i],
                                    cidr_block=PUBLIC_SUBNETS[i],
                                    map_public_ip_on_launch=True,
                                    vpc_id=myvpc.id)
        private_subnet = aws.ec2.Subnet(f"private-subnet-{i}",
                                        availability_zone=available.names[i],
                                        cidr_block=PRIVATE_SUBNETS[i],
                                        map_public_ip_on_launch=False,
                                        vpc_id=myvpc.id)
        public_subnets.append(public_subnet)
        private_subnets.append(private_subnet)

mygw = aws.ec2.InternetGateway("mygw",
    vpc_id=myvpc.id,
    tags={
        "Name": IGW_TAG_NAME,
    })

public_rt = aws.ec2.RouteTable("PublicRouteTable",
    vpc_id=myvpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block=PUBLIC_RT_CIDR,
            gateway_id=mygw.id,
        ),
    ],
    tags={
        "Name": PUBLIC_RT_TAG_NAME,
    })

private_rt = aws.ec2.RouteTable("PrivateRouteTable",
    vpc_id=myvpc.id,
    tags={
        "Name": PRIVATE_RT_TAG_NAME,
    })

for i, public_subnet in enumerate(public_subnets):
    aws.ec2.RouteTableAssociation(f"public-subnet-association-{i}",
                                  subnet_id=public_subnet.id,
                                  route_table_id=public_rt.id)

for i, private_subnet in enumerate(private_subnets):
    aws.ec2.RouteTableAssociation(f"private-subnet-association-{i}",
                                  subnet_id=private_subnet.id,
                                  route_table_id=private_rt.id)
