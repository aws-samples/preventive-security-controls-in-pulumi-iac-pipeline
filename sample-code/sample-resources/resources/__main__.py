#  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: MIT-0

#  Permission is hereby granted, free of charge, to any person obtaining a copy of this
#  software and associated documentation files (the "Software"), to deal in the Software
#  without restriction, including without limitation the rights to use, copy, modify,
#  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so.

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""An AWS Python Pulumi program"""
import os
import pulumi
import pulumi_aws
import sqs
import s3
import kms
import ec2
import ebs
import rds

app_config = pulumi.Config()
deploy_account_id = app_config.require("deploy_account_id")
deploy_role_name = app_config.require("deploy_role_name")
deploy_role_arn = "arn:aws:iam::" + deploy_account_id + ":role/" + deploy_role_name

aws_provider=pulumi_aws.Provider(
    "aws_role_provider",
    region="ap-southeast-1",
    assume_role = {
        "role_arn":deploy_role_arn,
        "session_name":"deploy"
    })

# Create an SQS queue
queue = sqs.create_sqs(aws_provider)
pulumi.export('queue_name', queue.id)

# Create an S3 bucket
s3.create_bucket(aws_provider)

# Create EC2 Security groups
ec2.create_security_groups(aws_provider)

# Create KMS keys
key = kms.create_keys(aws_provider)

# Create EBS volumes
ebs.create_ebs_volume(aws_provider, key)

# Create RDS instances
rds.create_rds_instance(aws_provider)
