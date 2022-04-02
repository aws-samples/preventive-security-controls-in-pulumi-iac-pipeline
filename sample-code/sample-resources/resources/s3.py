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

import pulumi
import json
from pulumi_aws import s3

def create_bucket(prov):
    bucket_1 = s3.Bucket('testing-bucket-for-public-access-block', pulumi.ResourceOptions(provider=prov))

    # S3 bucket with incorrect public access blocking and no secure transport policy and no encryption
    example_bucket_public_access_block_1 = s3.BucketPublicAccessBlock("BucketPublicAccessBlock-1",
        pulumi.ResourceOptions(provider=prov),
        bucket=bucket_1.id,
        block_public_acls=True,
        block_public_policy=True,
        ignore_public_acls=False,
        restrict_public_buckets=True)
    
    # S3 bucket with good configuration for public acccess blocking, secure transport policy and encryption
    bucket_2 = s3.Bucket('testing-bucket-for-tls', 
        pulumi.ResourceOptions(provider=prov), server_side_encryption_configuration=s3.BucketServerSideEncryptionConfigurationArgs(
            rule=s3.BucketServerSideEncryptionConfigurationRuleArgs(
                apply_server_side_encryption_by_default=s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                    sse_algorithm="AES256",
                ),
            )
        )
    )
    example_bucket_public_access_block_2 = s3.BucketPublicAccessBlock("BucketPublicAccessBlock-2",
        pulumi.ResourceOptions(provider=prov),
        bucket=bucket_2.id,
        block_public_acls=True,
        block_public_policy=True,
        ignore_public_acls=True,
        restrict_public_buckets=True)


    return 
