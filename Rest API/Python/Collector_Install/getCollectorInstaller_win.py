#!/usr/bin/env python

import requests
import json
import hashlib
import base64
import time
import hmac

# Account Info
AccessId = ''
AccessKey = ''
Company = ''

# Request Info
httpVerb = 'GET'
collectorId = '53'
collectorVersion = '34002'
resourcePath = '/setting/collector/collectors/' + \
    collectorId + '/installers/Win64'
queryParams = '?collectorVersion=' + collectorVersion
data = ''

# Construct URL
url = 'https://' + Company + '.logicmonitor.com/santaba/rest' + \
    resourcePath + queryParams

# Get current time in milliseconds
epoch = str(int(time.time() * 1000))

# Concatenate Request details
requestVars = httpVerb + epoch + resourcePath

# Construct signature
digest = hmac.new(
    AccessKey.encode('utf-8'),
    msg=requestVars.encode('utf-8'),
    digestmod=hashlib.sha256
).hexdigest()
signature = base64.b64encode(digest.encode('utf-8')).decode('utf-8')

# Construct headers
auth = 'LMv1 ' + str(AccessId) + ':' + str(signature) + ':' + epoch
headers = {'Content-Type': 'application/json',
           'Authorization': auth, 'X-Version': '3'}

# Make request
response = requests.get(url, data=data, headers=headers)

# Print response body if status code is not 200
if (response.status_code != 200):
    print('Response Body:', response.content)

else:
    file_ = open('LogicMonitorSetup.exe', 'wb')
    file_.write(response.content)
    file_.close()
    print('Collector installer has been downloaded successfully')
