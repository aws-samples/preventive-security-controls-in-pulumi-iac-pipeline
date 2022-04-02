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

# This script:
# 1. reads the CLI output of running the command 'pulumi preview' from an input file
# 2. Parses the contents and extracts the policy violations and writes them to 'metrics.json' 
#    as CloudWatch metrics object.

import os
import json
import time
import sys

if (len(sys.argv) != 2):
  print('The script needs the log output file name from crossguard check run as input')
  exit()

failed_policies = []
metrics = []
with open(sys.argv[1]) as File:
    start = False
    line = File.readline()
    while (line):
        if 'Policy Violations:' not in line and start != True:
            line = File.readline()
            continue
        else:
            line = File.readline().strip()
            start = True
            if '[mandatory]' in line:
                words = line.split('  ')
                failed_policy = words[2].split(' ')
                failed_policies.append(failed_policy[0])

            File.readline()
            File.readline()
            File.readline()

# For each policy violation, create a CloudWatch metric data object
for policy in failed_policies:
    metrics.append({
        'MetricName': policy,
        'Value':1,
        'Unit':'Count',
        'Timestamp':time.time(),
        'Dimensions':[
            {
                'Name':'Status',
                'Value':'Failed'
            },
            {
                'Name':'Author', 
                'Value':os.environ.get('AUTHOR')
            },
            {
                'Name':'Email', 
                'Value':os.environ.get('EMAIL')
            }
        ]
    })

# Write all metric data into a file
f = open('metrics.json', 'w')
json.dump(metrics, f, ensure_ascii=False)
f.close()