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

# Import individual policy definitions
from pyawsguard.eks_checks import default_log_types_policy
from pyawsguard.eks_checks import tags_policy
from pyawsguard.eks_checks import kms_key_for_encryption_policy
from pyawsguard.ebs_checks import ebs_encryption_policy
from pyawsguard.ec2_checks import secgrp_default_no_ingress
from pyawsguard.ec2_checks import secgrp_default_no_egress
from pyawsguard.ec2_checks import security_grp_ssh_policy_1
from pyawsguard.ec2_checks import security_grp_ssh_policy_2
from pyawsguard.kms_checks import kms_no_automatic_rotation
from pyawsguard.rds_checks import rds_deletion_protection_policy
from pyawsguard.s3_checks import s3_public_access_block
from pyawsguard.s3_checks import s3_ssl_requests
from pyawsguard.s3_checks import s3_encryption_policy
from pyawsguard.sqs_checks import sqs_no_public_access
from pyawsguard.vpc_checks import vpc_flow_logs_policy 

PolicyPack(
    name="aws-python",
    enforcement_level=EnforcementLevel.MANDATORY,
    policies=[
        s3_public_access_block,
        sqs_no_public_access,
        kms_no_automatic_rotation,
        vpc_flow_logs_policy,
        s3_encryption_policy,
        ebs_encryption_policy,
        rds_deletion_protection_policy,
        secgrp_default_no_ingress,
        secgrp_default_no_egress,
        security_grp_ssh_policy_1,
        security_grp_ssh_policy_2,
        s3_ssl_requests,
        default_log_types_policy,
        tags_policy,
        kms_key_for_encryption_policy,
    ],
)
