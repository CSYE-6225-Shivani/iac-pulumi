import pulumi
import pulumi_aws as aws

config = pulumi.Config()
cidr_block = config.require("vpc_cidr_block")
key_name = config.require("key_name")
instance_type = config.require("instance_type")
instance_ami = config.require("instance_ami")
asg_tag = config.require("asg_tag")
ec2_tag = config.require("ec2_tag")
igw_tag_name = config.require("igw_tag_name")
private_rt_tag_name = config.require("private_rt_tag_name")
private_subnet1 = config.require("private_subnet1")
private_subnet2 = config.require("private_subnet2")
private_subnet3 = config.require("private_subnet3")
public_rt_cidr = config.require("public_rt_cidr")
public_rt_tag_name = config.require("public_rt_tag_name")
public_subnet1 = config.require("public_subnet1")
public_subnet2 = config.require("public_subnet2")
public_subnet3 = config.require("public_subnet3")
sg_cidr = config.require("sg_cidr")
vpc_tag_name = config.require("vpc_tag_name")
ingress_port_1 = config.require("ingress_port_1")
ingress_port_2 = config.require("ingress_port_2")
ingress_port_3 = config.require("ingress_port_3")
ingress_port_4 = config.require("ingress_port_4")
egress_port = config.require("egress_port")
egress_cidr = config.require("egress_cidr")
delete_on_termination = config.require("delete_on_termination")
disable_api_termination = config.require("disable_api_termination")
volume_size = config.require("volume_size")
volume_type = config.require("volume_type")
rds_tag = config.require("rds_tag")
parameter_group_tag = config.require("parameter_group_tag")
rds_ingress_port_1 = config.require("rds_ingress_port_1")
rds_username = config.require("rds_username")
rds_password = config.require("rds_password")
rds_name = config.require("rds_name")
rds_engine = config.require("rds_engine")
rds_engine_version = config.require("rds_engine_version")
rds_instance_class = config.require("rds_instance_class")
rds_multi_az = config.require("rds_multi_az")
rds_allocated_storage = config.require("rds_allocated_storage")
rds_storage_type = config.require("rds_storage_type")
userdata_user = config.require("userdata_user")
userdata_group = config.require("userdata_group")
parameter_group_tag = config.require("parameter_group_tag")

PUBLIC_SUBNETS = [public_subnet1, public_subnet2, public_subnet3]
PRIVATE_SUBNETS = [private_subnet1, private_subnet2, private_subnet3]
available = aws.get_availability_zones(state="available")
public_subnets = []
private_subnets = []


myvpc = aws.ec2.Vpc("myvpc",
    cidr_block=cidr_block,
    tags={
        "Name": vpc_tag_name,
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
        "Name": igw_tag_name,
    })

public_rt = aws.ec2.RouteTable("PublicRouteTable",
    vpc_id=myvpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block=public_rt_cidr,
            gateway_id=mygw.id,
        ),
    ],
    tags={
        "Name": public_rt_tag_name,
    })

private_rt = aws.ec2.RouteTable("PrivateRouteTable",
    vpc_id=myvpc.id,
    tags={
        "Name": private_rt_tag_name,
    })

for i, public_subnet in enumerate(public_subnets):
    aws.ec2.RouteTableAssociation(f"public-subnet-association-{i}",
                                  subnet_id=public_subnet.id,
                                  route_table_id=public_rt.id)

for i, private_subnet in enumerate(private_subnets):
    aws.ec2.RouteTableAssociation(f"private-subnet-association-{i}",
                                  subnet_id=private_subnet.id,
                                  route_table_id=private_rt.id)
    

application_sg = aws.ec2.SecurityGroup("application_security_group",
    description="Allow TLS inbound traffic",
    vpc_id=myvpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow traffic on port 22",
            from_port=ingress_port_1,
            to_port=ingress_port_1,
            protocol="tcp",
            cidr_blocks=[sg_cidr],
            ),
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow traffic on port 80",
            from_port=ingress_port_2,
            to_port=ingress_port_2,
            protocol="tcp",
            cidr_blocks=[sg_cidr],
            ),
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow traffic on port 443",
            from_port=ingress_port_3,
            to_port=ingress_port_3,
            protocol="tcp",
            cidr_blocks=[sg_cidr],
            ),
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow traffic on port 5000",
            from_port=ingress_port_4,
            to_port=ingress_port_4,
            protocol="tcp",
            cidr_blocks=[sg_cidr],
            ),
        ],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        from_port=egress_port,
        to_port=egress_port,
        protocol="-1",
        cidr_blocks=[egress_cidr],
    )],
    tags={
        "Name": asg_tag,
    })


database_sg = aws.ec2.SecurityGroup("database_security_group",
    description="Allow PostgreSQL traffic",
    vpc_id=myvpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            description="Allow traffic on port 5432",
            from_port=rds_ingress_port_1,
            to_port=rds_ingress_port_1,
            protocol="tcp",
            security_groups=[application_sg.id]
            ),
        ],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        from_port=egress_port,
        to_port=egress_port,
        protocol="-1",
        cidr_blocks=[egress_cidr],
    )],
    tags={
        "Name": rds_tag,
    })


db_parameter_group = aws.rds.ParameterGroup("db-parameter-group",
    family="postgres15",
    tags={
        "Name" : parameter_group_tag,
    })


private_subnet_ids = [subnet.id for subnet in private_subnets]
rds_subnet_group = aws.rds.SubnetGroup("rds_subnet_group",
                                       subnet_ids=private_subnet_ids,
                                       description="csye6225 RDS Subnet Group",
                                       name="csye6225-rds-subnet-group")



rds_instance = aws.rds.Instance("rds_instance",
    db_name=rds_name,
    allocated_storage=rds_allocated_storage,
    storage_type=rds_storage_type,
    engine=rds_engine,
    engine_version=rds_engine_version,
    instance_class=rds_instance_class,
    identifier=rds_name,
    multi_az=rds_multi_az,
    parameter_group_name=db_parameter_group.name,
    password=rds_password,
    db_subnet_group_name = rds_subnet_group.name,
    username=rds_username,
    skip_final_snapshot= True,
    vpc_security_group_ids = [database_sg.id])



def user_data(endpoint):
    user_data = f'''#!/bin/bash
ENV_FILE="/opt/webapp.properties"
echo "RDS_HOSTNAME={endpoint}" > ${{ENV_FILE}}
echo "RDS_USERNAME={rds_username}" >> ${{ENV_FILE}}
echo "RDS_PASSWORD={rds_password}" >> ${{ENV_FILE}}
echo "DATABASE_URL=postgresql://{rds_username}:{rds_password}@{endpoint}/webapp" >> ${{ENV_FILE}}
$(sudo chown {userdata_user}:{userdata_group} ${{ENV_FILE}})
$(sudo chmod 400 ${{ENV_FILE}})
$(sudo chown -R {userdata_user}:{userdata_group} /opt/webapp)
$(sudo chown {userdata_user}:{userdata_group} /opt/users.csv)
$(sudo systemctl start webapp)
'''
    return user_data
 

generate_user_data = rds_instance.endpoint.apply(user_data)


root_block_device = aws.ec2.InstanceRootBlockDeviceArgs(
    volume_size=volume_size,  # Root Volume Size
    volume_type=volume_type,  # Root Volume Type
    delete_on_termination=delete_on_termination,
)

# Create IAM role for CloudWatch
cloudwatch_role = aws.iam.Role("my-cloudwatch-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                }
            }
        ]
    }""",
)

# Attach CloudWatchAgentServer policy to cloudwatch_role

policy_attachment = aws.iam.PolicyAttachment("my-cloudwatch-policy",
    policy_arn="arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy",
    roles=[cloudwatch_role.name],
)

# Create an IAM instance profile
cloudwatch_instance_profile = aws.iam.InstanceProfile("my-cloudwatch-instance-profile",
    role=cloudwatch_role.name,  # Associate the role with the instance profile
)

# Create an EC2 instance
EC2_instance = aws.ec2.Instance("my-instance",
    ami=instance_ami,  # custom AMI ID
    key_name=key_name,
    instance_type=instance_type,
    vpc_security_group_ids=[application_sg.id],  # Attach the security group
    subnet_id=public_subnet.id,  # Specify the subnet ID
    root_block_device= root_block_device,
    user_data=generate_user_data,
    opts=pulumi.ResourceOptions(depends_on=[rds_instance]),
    iam_instance_profile=cloudwatch_instance_profile.name,
    disable_api_termination=disable_api_termination,  # Protect against accidental termination
    tags={
        "Name": ec2_tag,
    },
)
