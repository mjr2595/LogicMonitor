#!/usr/bin/python

import os
import requests
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()  # take environment variables from .env

# Account Info
portal = os.getenv("PORTAL")
bearer = os.getenv("BEARER")

# Request Info: Get all devices
httpVerb = 'GET'
resourcePath = '/device/devices'
queryParams = '?fields=id,displayName'

# Construct URL
url = 'https://' + portal + '.logicmonitor.com/santaba/rest' + \
    resourcePath + queryParams

# Construct headers
auth = 'bearer ' + bearer
headers = {'Content-Type': 'application/json',
           'X-version': '3', 'Authorization': auth}

# Make request
response = requests.get(url, headers=headers, verify=True)
response_json = response.json()

# Print response
pprint(str(response_json))
