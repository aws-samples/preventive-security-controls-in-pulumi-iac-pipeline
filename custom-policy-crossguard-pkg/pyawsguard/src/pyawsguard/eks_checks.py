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

import pulumi_aws as aws
import json
import time
import datetime
import os

def default_log_types_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:eks/cluster:Cluster":
        if "enabled_cluster_log_types" not in args.props or args.props["enabled_cluster_log_types"] is None:
            report_violation(
                "EKS Cluster should have all three log types (api, audit, authenticator) enabled by default")
        else:
            logTypes = args.props["enabledClusterLogTypes"]
            if len(logTypes) < 3:
                report_violation(
                    "EKS Cluster should have all three log types (api, audit, authenticator) enabled by default")
            elif "api" not in logTypes or "audit" not in logTypes or "authenticator" not in logTypes:
                report_violation(
                    "EKS Cluster should have all three log types (api, audit, authenticator) enabled by default")

default_log_types_policy = ResourceValidationPolicy(
    name="eks-cluster-default-logs",
    description="Validating if EKS Cluster has all three log types enabled by default",
    validate=default_log_types_validator,
)

def tags_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:eks/cluster:Cluster":
        if "tags" not in args.props or args.props["tags"] is None:
            report_violation("EKS Cluster should have default tags")
        else:
            tags = args.props["tags"]
            if "Name" not in tags or "env" not in tags or tags["Name"] is None or tags["env"] is None:
                report_violation("EKS Cluster should have default tags")

tags_policy = ResourceValidationPolicy(
    name="eks-cluster-tags_policy",
    description="Validating if EKS Cluster has tags by default",
    validate=tags_validator,
)

def kms_key_for_encryption_validator(args: ResourceValidationArgs, report_violation: ReportViolation):
    if args.resource_type == "aws:eks/cluster:Cluster": 
        if "encryption_config_key_arn" not in args.props or args.props["encryption_config_key_arn"] is None:
            report_violation(
                "Kubernetes Services should have AWS KMS key configured for encryption of secrets")

kms_key_for_encryption_policy = ResourceValidationPolicy(
    name="eks-cluster-kms-key",
    description="Validating if EKS Cluster has AWS KMS key configured",
    validate=kms_key_for_encryption_validator,
)

