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
import pulumi_aws as aws


def create_ebs_volume(prov, key_enc):
    # EBS volume with encryption not enabled
    example = aws.ebs.Volume("ebsVolumeBad",
    pulumi.ResourceOptions(provider=prov),
    availability_zone="ap-southeast-1a",
    size=40,
    encrypted=None,
    kms_key_id=None,
    tags={
        "Name": "TestVolumeNoEnc",
    })

    # EBS volume with encryption enabled
    example_2 = aws.ebs.Volume("ebsVolumeGood",
    pulumi.ResourceOptions(provider=prov),
    availability_zone="ap-southeast-1b",
    size=40,
    encrypted=True,
    kms_key_id=key_enc.arn,
    tags={
        "Name": "TestVolumeWithEnc",
    })

    return