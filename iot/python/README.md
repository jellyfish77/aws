# AWS IoT Python

## AWS IoT

https://docs.aws.amazon.com/iot/latest/developerguide/what-is-aws-iot.html

## Install Python Boto3 AWS Library (AWS SDK for Python)

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

	pip install boto3

## Boto3 Examples

https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python.html

## AWS Config

https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

### Credentials Values

Run following command:

	aws configure

When you type this command, the AWS CLI prompts you for four pieces of information (access key, secret access key, AWS Region, and output format), and stores them in a profile (a collection of settings) named default. This profile is then used any time you run an AWS CLI command that doesn't explicitly specify a profile to use.

Set the following :

- aws_access_key_id = (obtain from AWS)
- aws_secret_access_key = (obtain from AWS)
- output = json
- region = us-west-2

### AWS Config Files

Config is stored in these files:

- ~/.aws/config
- ~/.aws/credentials

## Execute

	./simulate-random-moisture-levels.py 
