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

def create_security_groups(prov):
    # VPC creation
    mainvpc = aws.ec2.Vpc("test-vpc", 
    pulumi.ResourceOptions(provider=prov), cidr_block="10.1.0.0/16")

    # Security Group that enables SSH traffic from all IP addresses
    allow_ssh_bad = aws.ec2.SecurityGroup("allowSSH",
    pulumi.ResourceOptions(provider=prov),
        # Allow SSH inbound traffic",
        vpc_id=mainvpc.id,
        ingress=[
            aws.ec2.SecurityGroupIngressArgs(
                description="SSH ingress from VPC",
                from_port=22,
                to_port=22,
                protocol="tcp",
                cidr_blocks=["0.0.0.0/0"],
                ipv6_cidr_blocks=["::/0"],
            )
        ],
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                description="SSH egress from VPC",
                from_port=0,
                to_port=0,
                protocol="-1",
                cidr_blocks=["0.0.0.0/0"],
                ipv6_cidr_blocks=["::/0"],
            )
        ],
    )

    # Security Group that allows only TLS traffic
    allow_tls_good = aws.ec2.SecurityGroup("allowTls",
        pulumi.ResourceOptions(provider=prov),
        description="Allow TLS inbound traffic",
        vpc_id=mainvpc.id,
    )
    tls_secgrp_ingress_rule = aws.ec2.SecurityGroupRule("tls_secgrp_ingress_rule",
        pulumi.ResourceOptions(provider=prov),
        type="ingress",
        from_port=443,
        to_port=443,
        protocol="tcp",
        cidr_blocks=["0.0.0.0/0"],
        security_group_id=allow_tls_good.id
    )

    # Default Security Group that allows all ingress
    defaultSecGrp = aws.ec2.DefaultSecurityGroup("defaultSecGrp",
        pulumi.ResourceOptions(provider=prov),
        vpc_id=mainvpc.id,
        ingress=[aws.ec2.DefaultSecurityGroupIngressArgs(
            from_port=0,
            to_port=0,
            protocol="-1",
            self=True,
        )],
        egress=[aws.ec2.DefaultSecurityGroupEgressArgs(
            from_port=0,
            to_port=0,
            protocol="-1",
            cidr_blocks=["0.0.0.0/0"],
        )]
    )

    # VPC Flow logs creation
    example_log_group = aws.cloudwatch.LogGroup("vpcFlowLogGroup", pulumi.ResourceOptions(provider=prov))
    example_role = aws.iam.Role("exampleRole", pulumi.ResourceOptions(provider=prov), assume_role_policy="""{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
            "Service": "vpc-flow-logs.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
        }
    ]
    }
    """)
    example_flow_log = aws.ec2.FlowLog("exampleFlowLog",
        pulumi.ResourceOptions(provider=prov),
        iam_role_arn=example_role.arn,
        log_destination=example_log_group.arn,
        traffic_type="ALL",
        vpc_id=mainvpc.id
    )
    example_role_policy = aws.iam.RolePolicy("exampleRolePolicy",
        pulumi.ResourceOptions(provider=prov),
        role=example_role.id,
        policy="""{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "logs:DescribeLogGroups",
            "logs:DescribeLogStreams"
        ],
        "Effect": "Allow",
        "Resource": "*"
        }
    ]
    }
    """)

    return

