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
httpVerb ='GET'
resourcePath = '/device/devices'
data = ''

#Construct URL 
url = 'https://'+ Company +'.logicmonitor.com/santaba/rest' + resourcePath

#Get current time in milliseconds
epoch = str(int(time.time() * 1000))

#Concatenate Request details
requestVars = httpVerb + epoch + data + resourcePath

#Construct signature
signature = base64.b64encode(hmac.new(AccessKey,msg=requestVars,digestmod=hashlib.sha256).hexdigest())

#Construct headers
auth = 'LMv1 ' + AccessId + ':' + signature + ':' + epoch
headers = {'Content-Type':'application/json','Authorization':auth,'X-Version':'2'}

#Make request
response = requests.get(url, data=data, headers=headers)

#Print status and body of response
print 'Response Status:',response.status_code
print 'Response Body:',response.content