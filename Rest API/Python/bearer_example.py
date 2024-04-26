#!/usr/bin/python

import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

# Account Info
portal = os.getenv("PORTAL")
bearer = os.getenv("BEARER")

# Request Info: Get all devices
httpVerb = 'GET'
resourcePath = '/device/devices'

# Dynamic queryParams
size = 1
offset = 0
queryParams = f'?fields=id,displayName&size={size}&offset={offset}'

# Construct URL
url = f'https://{portal}.logicmonitor.com/santaba/rest{resourcePath}{queryParams}'

# Construct headers
auth = 'bearer ' + bearer
headers = {'Content-Type': 'application/json',
           'X-version': '3', 'Authorization': auth}

# Make request
response = requests.get(url, headers=headers, verify=True, timeout=15)
response_json = response.json()

# Print response
pprint(str(response_json))
