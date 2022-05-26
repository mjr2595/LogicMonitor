#!/bin/env python3
#* © 2007-2018 - LogicMonitor, Inc.  All rights reserved.
#* Author Jonathan Arnold - Solutions Engineer

# Account Info
access_id = ''
access_key = ''
company = ''
debug_command = "!tlist summary=true"


def send_debug_command(access_id, access_key, company, debug_command):
    import requests
    import json
    import hashlib
    import base64
    import time
    import hmac

    # Request Info: Add a service
    http_verb = 'POST'
    resource_path = '/debug'
    data = '{"cmdline":"' + debug_command + '"}'
    query_params = "?v=2&collectorId=1"

    # Construct URL
    url = 'https://' + company + '.logicmonitor.com/santaba/rest' + \
        resource_path + query_params

    # Get current time in milliseconds
    epoch = str(int(time.time() * 1000))

    # Concatenate Request details
    request_vars = http_verb + epoch + data + resource_path

    # Construct signature
    hmac = hmac.new(access_key.encode(), msg=request_vars.encode(),
                     digestmod=hashlib.sha256).hexdigest()
    signature = base64.b64encode(hmac.encode())

    # Construct headers
    auth = 'LMv1 ' + access_id + ':' + signature.decode() + ':' + epoch
    headers = {'Content-Type': 'application/json', 'Authorization': auth}

    # Make request
    response = requests.post(url, data=data, headers=headers)

    # Print status and body of response
    body_json = response.json()
    session_id = body_json['sessionId']
    return session_id


def get_debug_results(access_id, access_key, company, session_id):
    import requests
    import json
    import hashlib
    import base64
    import time
    import hmac

    # Request Info
    http_verb = 'GET'
    resource_path = '/debug/' + session_id
    query_params = "?v=2&collectorId=1"
    data = ''

    # Construct URL
    url = 'https://' + company + '.logicmonitor.com/santaba/rest' + \
        resource_path + query_params

    # Get current time in milliseconds
    epoch = str(int(time.time() * 1000))

    # Concatenate Request details
    request_vars = http_verb + epoch + data + resource_path

    # Construct signature
    hmac = hmac.new(access_key.encode(), msg=request_vars.encode(),
                    digestmod=hashlib.sha256).hexdigest()
    signature = base64.b64encode(hmac.encode())

    # Construct headers
    auth = 'LMv1 ' + access_id + ':' + signature.decode() + ':' + epoch
    headers = {'Content-Type': 'application/json', 'Authorization': auth}

    # Make request
    response = requests.get(url, data=data, headers=headers)

    # Print status and body of response
    return response.json()


session_id = send_debug_command(access_id, access_key, company, debug_command)

debug_results = get_debug_results(access_id, access_key, company, session_id)

print(debug_results)