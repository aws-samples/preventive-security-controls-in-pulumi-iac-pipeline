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

from pyawsguard.metric_object import metric


###################################
# EC2 - Security Groups
###################################
# Default Security Group Ingress rules validator
def secgrp_default_no_ingress_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:ec2/defaultSecurityGroup:DefaultSecurityGroup":
        if "ingress" in args.props and args.props["ingress"] != None and (len(args.props["ingress"]) > 0):
            report_violation(
                "There should be no Ingress rules in the VPC's Default security group " + args.name)

secgrp_default_no_ingress = ResourceValidationPolicy(
    name="secgrp-default-no-ingress",
    description="Validating that the default security group of VPC has ingress rules",
    validate=secgrp_default_no_ingress_validator,
)

# Default Security Group Egress rules validator
def secgrp_default_no_egress_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:ec2/defaultSecurityGroup:DefaultSecurityGroup":
        if "egress" in args.props and args.props["egress"] != None and (len(args.props["egress"]) > 0):
            report_violation(
                "There should be no Egress rules in the VPC's Default security group " + args.name)

secgrp_default_no_egress = ResourceValidationPolicy(
    name="secgrp-default-no-egress",
    description="Validating that the default security group of VPC has egress rules",
    validate=secgrp_default_no_egress_validator,
)

# Security Group SSH Ingress rules validator
def security_grp_ssh_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:ec2/securityGroup:SecurityGroup": 
        if "ingress" in args.props:
            for ingress_rule in args.props["ingress"]:
                if int(ingress_rule["fromPort"]) == 22 and int(ingress_rule["toPort"]) == 22 and ingress_rule["cidrBlocks"][0] == "0.0.0.0/0":
                    report_violation(
                        "This Security group " + args.name + " has allowed SSH access from all addresses."
                    )
                    break

security_grp_ssh_policy_1 = ResourceValidationPolicy(
    name="security-group-ssh-policy",
    description="Validating if port 22 is open to all IPs for incoming SSH connections.",
    validate=security_grp_ssh_validator,
)

# Security Group Rules Ingress validator
def security_grp_rule_ssh_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:ec2/securityGroupRule:SecurityGroupRule": 
        if "type" in args.props and args.props["type"] == "ingress":
            if int(args.props["fromPort"]) == 22 and int(args.props["toPort"]) == 22 and args.props["cidrBlocks"][0] == "0.0.0.0/0":
                report_violation(
                    "This Security group " + args.name + " has allowed SSH access from all addresses " 
               )

security_grp_ssh_policy_2 = ResourceValidationPolicy(
    name="security-group-ssh-policy",
    description="Validating if port 22 is open to all IPs for incoming SSH connections.",
    validate=security_grp_rule_ssh_validator,
)