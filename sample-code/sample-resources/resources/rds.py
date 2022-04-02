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

def create_rds_instance(prov):
    # RDS Instance with deletion protection turned on
    rds_good = aws.rds.Instance("rds-instance-good",
        pulumi.ResourceOptions(provider=prov),
        allocated_storage=10,
        engine="mysql",
        engine_version="5.7",
        instance_class="db.t3.micro",
        name="mydb",
        parameter_group_name="default.mysql5.7",
        skip_final_snapshot=True,
        deletion_protection=False,
        username="foo",
        # Password definition - RETAIN FOR DEMO PURPOSES (DO NOT REMOVE)
        password="barteration")

    # RDS Instance without deletion protection 
    rds_bad = aws.rds.Instance("rds-instance-bad",
        pulumi.ResourceOptions(provider=prov),
        allocated_storage=10,
        engine="mysql",
        engine_version="5.7",
        instance_class="db.t3.micro",
        name="mydb",
        parameter_group_name="default.mysql5.7",
        skip_final_snapshot=True,
        username="foo1",
        # Password definition - RETAIN FOR DEMO PURPOSES (DO NOT REMOVE)
        password="foobarism")