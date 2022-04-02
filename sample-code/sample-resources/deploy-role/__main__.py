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

import json
import os
import pulumi
import pulumi_aws as aws

aws_config = pulumi.Config("aws")
aws_region = aws_config.require("region")

caller = aws.get_caller_identity()
source_account_id = caller.account_id

app_config = pulumi.Config()
deploy_account_id = app_config.require("deploy_account_id")
deploy_role_name = app_config.require("deploy_role_name")

deploy_role_arn = "arn:aws:iam::" + deploy_account_id + ":role/" + deploy_role_name

aws_provider=aws.Provider(
    "aws_role_provider",
    region="ap-southeast-1",
    assume_role = {
        "role_arn":deploy_role_arn, 
        "session_name":"deploy"
    })

deploy_policy = aws.iam.Policy(
    "deploy_policy",
    pulumi.ResourceOptions(provider=aws_provider),
    path = "/",
    name = "sample-other-services-deploy",
    description = "Provides required access to deploy other services",
    policy=json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [{
                "Action": [
                    "ec2:*",
                    "kms:*",
                    "rds:*",
                    "sqs:*",
                    "s3:*",
                    "logs:*",
                    "iam:*"
                ],
                "Effect": "Allow",
                "Resource": "*",
            }],
        }
    ))

deploy_role = aws.iam.Role(
    "deploy_role",
    pulumi.ResourceOptions(provider=aws_provider),
    name="sample-other-services-deploy",
    managed_policy_arns =
    [
        deploy_policy.arn
    ],
    assume_role_policy = json.dumps(
        {
            "Version": "2012-10-17",
            "Statement":
            [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "arn:aws:iam::{}:root".format(source_account_id)
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    ))
