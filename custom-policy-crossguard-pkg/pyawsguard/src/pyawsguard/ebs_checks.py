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
import os
import datetime

###################################
# EBS Volume
###################################
# EBS Encryption validator
def ebs_encryption_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:ebs/volume:Volume": 
        if "encrypted" not in args.props:
            log.error("ebs,"+args.name + ",encrypted,false")
            report_violation(
                "Encryption is not enabled for the EBS Volume " + args.name )
        elif args.props["encrypted"] != True:
            log.error(args.name + "\tencrypted\tfalse")
            report_violation(
                "Encryption is not enabled for the EBS Volume " + args.name )

ebs_encryption_policy = ResourceValidationPolicy(
    name="ebs_encryption_policy",
    description="Validating encryption configuration on EBS volumes.",
    validate=ebs_encryption_validator,
)