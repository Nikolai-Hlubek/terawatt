#!/usr/bin/env python3
import sys
import re

data=sys.stdin.readlines()

result=[('time', 'uii')]
for d in data:
    timestamp=re.findall('timestamp":\d+', d)[0].replace('timestamp":', '')
    for r in re.findall('uii":"[^"]+', d):
        result.append((timestamp, r.replace('uii":"', '')))

for r in result:
    print(r[0]+', '+r[1])
