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

from pulumi_policy import (
    EnforcementLevel,
    PolicyPack,
    ReportViolation,
    ResourceValidationArgs,
    ResourceValidationPolicy,
)

from pulumi import log

import pulumi_aws as aws
import json
import time
import datetime
import os

###################################
# S3
###################################
# S3 Public Access Block validator
def s3_public_access_block_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:s3/bucketPublicAccessBlock:BucketPublicAccessBlock":         
        block_public_acls = args.props["blockPublicAcls"]
        block_public_policy = args.props["blockPublicPolicy"]   
        ignore_public_acls = args.props["ignorePublicAcls"]
        restrict_public_buckets = args.props["restrictPublicBuckets"]
        if not block_public_acls or not block_public_policy or not ignore_public_acls or not restrict_public_buckets:
            report_violation(
                "Public access is not blocked for the bucket " + args.name )
                #"Read more about blocking public access here: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html")

s3_public_access_block = ResourceValidationPolicy(
    name="s3_public_access_block",
    description="Validating the publicRead or publicReadWrite permission on AWS S3 buckets.",
    validate=s3_public_access_block_validator,
)

# S3 Bucket policy validator
def s3_ssl_requests_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:s3/bucketPolicy:BucketPolicy":
        f = open('data.txt', 'w')
        if "policy" in args.props:
            flag = 0
            policy = json.loads(args.props["policy"])
            if "Statement" in policy:
                for stmt in policy["Statement"]:
                    print(stmt["Condition"])
                    print(stmt["Condition"]["Bool"])
                    if "Condition" in stmt and "Bool" in stmt["Condition"] and "aws:SecureTransport" in stmt["Condition"]["Bool"] and stmt["Condition"]["Bool"]["aws:SecureTransport"] == "false":
                        flag = 1
                        break
                if flag == 0:
                    report_violation("S3 Secure transport flag is not set in bucket policy for " + args.name )
            else:
                report_violation("No statements found in policy " + args.name )
        else:
            report_violation("No policy found in " + args.name )


s3_ssl_requests = ResourceValidationPolicy(
    name="s3-ssl-requests-policy",
    description="Validating that S3 buckets have TLS checks in bucket policy.",
    validate=s3_ssl_requests_validator,
)

# S3 Encryption validator
def s3_encryption_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:s3/bucket:Bucket":
        if "serverSideEncryptionConfiguration" not in args.props or args.props["serverSideEncryptionConfiguration"] == None:
            report_violation(
                "Default encryption is not enabled for the S3 bucket " + args.name )

s3_encryption_policy = ResourceValidationPolicy(
    name="s3_encryption_policy",
    description="Validating default encryption configuration on AWS S3 buckets.",
    validate=s3_encryption_validator,
)