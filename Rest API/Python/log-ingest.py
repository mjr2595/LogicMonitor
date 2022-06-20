#!/usr/bin/env python

import requests
import json
import hashlib
import base64
import time
import hmac

#Account Info
AccessId =''
AccessKey =''
Company = ''

#Request Info
httpVerb = 'POST'
resourcePath = '/log/ingest'
data = '{msg: "user john logged in",timestamp: 1582555792,_lm.resourceId: {system.deviceId: "281"},host: "systemY",username: "john",type_of_auth: "oauth"}'
queryParams = ''

#Construct URL 
url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath + queryParams

#Get current time in milliseconds
epoch = str(int(time.time() * 1000))

#Concatenate Request details
requestVars = httpVerb + epoch + data + resourcePath 

#Construct signature
digest = hmac.new(
        AccessKey.encode('utf-8'),
        msg=requestVars.encode('utf-8'),
        digestmod=hashlib.sha256
).hexdigest()
signature = base64.b64encode(digest.encode('utf-8')).decode('utf-8')

#Construct headers
auth = 'LMv1 ' + AccessId + ':' + str(signature) + ':' + epoch
headers = {'Content-Type':'application/json','Authorization':auth,'X-Version':'2'}

#Make request
response = requests.post(url, data=data, headers=headers)

#Print status and body of response
print(httpVerb + ' ' + url)
print('Response Status:',response.status_code)
print('Response Body:',response.content)