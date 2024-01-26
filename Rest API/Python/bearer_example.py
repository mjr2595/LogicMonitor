#!/usr/bin/python

import requests
import json

# Account Info
portal = 'portalname'
bearer = 'lmb_xxx'

# Request Info: Get all devices
httpVerb = 'GET'
resourcePath = '/device/devices'
queryParams = ''

# Construct URL
url = 'https://' + portal + '.logicmonitor.com/santaba/rest' + \
    resourcePath + queryParams
print(url)

# Construct headers
auth = 'bearer ' + bearer
headers = {'Content-Type': 'application/json',
           'X-version': '3', 'Authorization': auth}

# Make request
response = requests.get(url, headers=headers, verify=True)

# Print status of response and save response body to file
print(f"Response Status: {response.status_code}")
print(f"Response Content: {response.content}")
