#!/usr/bin/python

import os
from pprint import pprint
import requests
from dotenv import load_dotenv

load_dotenv()

# Account Info
portal = os.getenv("PORTAL")
bearer = os.getenv("BEARER")

resourcePath = '/website/websites/21'
queryParams = ''
data = '{"properties":[{"name":"test_prop","value":"updated by API"}]}'

# Construct URL
url = 'https://' + portal + '.logicmonitor.com/santaba/rest' + \
    resourcePath + queryParams

# Construct headers
auth = 'bearer ' + bearer
headers = {'Content-Type': 'application/json',
           'X-version': '3', 'Authorization': auth}

# Make request
response = requests.patch(
    url, data=data, headers=headers, verify=True, timeout=15)
response_json = response.json()

# Print response
pprint(str(response_json))
