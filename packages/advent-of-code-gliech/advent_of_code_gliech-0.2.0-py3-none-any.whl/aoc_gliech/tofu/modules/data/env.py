#!/usr/bin/env python3
import json
import os
import sys

query = json.load(sys.stdin)
print(json.dumps({var: os.environ.get(var) for var in query["vars"].split(",")}))
