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
httpVerb = 'PATCH'
resourcePath = '/device/devices/281'
data = '{"customProperties":[{"name":"alert","value":"true"}]}'

# Construct URL
url = 'https://' + Company + '.logicmonitor.com/santaba/rest' + resourcePath

# Get current time in milliseconds
epoch = str(int(time.time() * 1000))

# Concatenate Request details
requestVars = httpVerb + epoch + data + resourcePath

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
response = requests.patch(url, data=data, headers=headers)

# Print status and body of response
print('Response Status:', response.status_code)
print('Response Body:', response.content)
