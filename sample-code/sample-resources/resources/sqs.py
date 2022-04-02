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

def create_sqs(prov):
    queue = aws.sqs.Queue("test_queue2", 
        pulumi.ResourceOptions(provider=prov), fifo_queue=False)

    test = aws.sqs.QueuePolicy("test_queuepolicy",
        pulumi.ResourceOptions(provider=prov),
        queue_url=queue.id,
        # Too permissive queue policy
        policy="{\"Version\": \"2012-10-17\",\"Id\": \"sqspolicy\",\"Statement\": [{\"Sid\": \"First\",\"Effect\": \"Allow\",\"Principal\": \"*\",\"Action\":\"sqs:SendMessage\",\"Resource\": \"*\"}]}")
        # Limited policy - COMMENTED FOR DEMO PURPOSES (DO NOT REMOVE)
        #policy="{\"Version\": \"2012-10-17\",\"Id\": \"sqspolicy\",\"Statement\": [{\"Sid\": \"First\",\"Effect\": \"Allow\",\"Principal\": \"arn:aws:iam::880599700200:root\",\"Action\":\"sqs:SendMessage\",\"Resource\": \"*\"}]}")
    return queue

    