# iac-pulumi
## INFRASTRUCTURE AS CODE USING PULUMI
This code creates infrastructure based on profile and AWS information provided in its config file.

Below are the resources that gets created through this code:

            1. Virtual Private Cloud
            2. Internet Gateway
            3. Private Route Table
            4. Public Route Table
            5. Private subnets associated with Private Route Table
            6. Public subnets associated with Public Route Table
            7. CloudWatch Role
            8. CloudWatch Policy
            9. CloudWatch Instance Profile
            10. Application Security Group
            11. Database/RDS Security Group
            12. Database Parameter Group
            13. RDS Subnet Group (private subnets)
            14. RDS instance associated with DB Paramater Group, DB Security Group, and RDS Subnet Group
            15. EC2 Instance
            16. A Record for EC2 instance

## PREREQUISITES FOR RUNNING LOCALLY:
- Pulumi: https://www.pulumi.com/docs/install/
- AWS account with an organization - Add 2 accounts (dev & demo) in the organization and create admin users for each, generate AWS Access & Secret keys for both
- AWS CLI
- AWS configure setup from aws cli(profile for dev and demo accounts)

         -> aws configure –profile=dev
         -> aws configure –profile=demo
- Add access key, secret key, and nearest region here to configure your profiles
- Now to work under any profile, pass this variable first:

        - Mac:
          export AWS_PROFILE=<dev/demo>

        - Windows:
          setx AWS_PROFILE <dev/demo>


## STEPS TO FOLLOW
- Clone the repo - git clone <link>
- Check whether pulumi is installed or not - pulumi version
- Check available stacks 
       
        pulumi stack ls
- If no stacks are available, create one using below command and then follow along:

        pulumi new aws-python
- Change which profile to build your stack in using below command:
        
        pulumi config set aws:profile <dev/demo>
- Select a stack from multiple stacks:
        
        pulumi stack select <name>
- To change any of the variables defined in the pulumi config, use below command:


       pulumi config set <variable_name> <value>

- As of now, we have following variables defined in our pulumi config file:

        - aws:profile
        - aws:region
        - A_Record_TTL
        - A_Record_name
        - asg_tag
        - delete_on_termination
        - ec2_tag
        - egress_cidr
        - egress_port
        - hosted_zone_id
        - igw_tag_name
        - ingress_port_1
        - ingress_port_2
        - ingress_port_3
        - ingress_port_4
        - instance_ami
        - instance_type
        - key_name
        - private_rt_tag_name
        - private_subnet1
        - private_subnet2
        - private_subnet3
        - public_rt_cidr
        - public_rt_tag_name
        - public_subnet1
        - public_subnet2
        - public_subnet3
        - sg_cidr
        - volume_size
        - volume_type
        - vpc_cidr_block
        - vpc_tag_name

- Once everything look okay, run below command to build your infrastructure:
        
       pulumi up

- To destroy everything, run below command:
        
       pulumi destroy
