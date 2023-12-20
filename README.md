# Cloud-Native Flask API on AWS using IaC

This repository contains code for building the infrastructure on AWS through Pulumi.

## Use with Related Repositories

1. [webapp](https://github.com/CSYE-6225-Shivani/webapp): Contains IaC code for developing AMI containing flask based webapp.
2. [serverless](https://github.com/CSYE-6225-Shivani/serverless): Contains code for Lambda function that needs to be zipped in this repository for it to run successfully.

## Tech Stack

| **Category**                 | **Technology/Tool**                                     |
|------------------------------|---------------------------------------------------------|
| **Programming Language**     | Python (Flask)                                           |
| **Database**                 | PostgreSQL                                              |
| **Cloud Services**           | AWS (EC2, RDS, VPC, IAM, Route53, CloudWatch, SNS, Lambda, ELB, ASG) |
| **Infrastructure as Code**   | Pulumi                                                  |
| **Image Creation**           | Packer (Custom AMIs)                                     |
| **Version Control**          | Git                                                     |
| **CI/CD**                    | GitHub Actions                                          |
| **Additional Tools**         | Mailgun, Google Cloud Platform (GCP)                     |

## Read through [pulumi](./pulumi.md) documentation for detailed information on setting up pulumi respository.


## Setting up webapp, iac-pulumi, and serverless repositiories
1. Clone webapp repository (assuming that it is set up as guided in its documentation)
2. Clone iac-pulumi repository and follow documentation in [pulumi](./pulumi.md)
3. Clone serverless respository and follow instructions in its README.md

## How do these repositories work together:
> Clone all three repositories. You just need to have prerequisites for pulumi on your local.

1. Set up everything as explained in [pulumi](./pulumi.md) locally
2. You need to have following things on your system:
     - Pulumi
     - AWS CLI
3. Go to the folder where serverless repository folder exist and run below command for each package mentioned in its requirements.txt:
    
       pip install --target ./serverless/ <package_name>
4. Once all the packages have been installed, select all the files in the serverless folder and compress them to create a zip file (The name that you give to this file should be passed as an environment variable in pulumi config file with .zip extension)

5. Go to iac-pulumi folder and copy the zip file created in the previous step in this folder

6. Run the `pulumi up` command from your pulumi code folder and it should build your infrastructure (verify that `instance_ami` passed in the pulumi config file is valid)

7. Once the infrastructure is up, if you now push any changes to webapp repository and merge the pull request, GitHub Worflow Action will automatically change AMI used by ASG to the newly built AMI