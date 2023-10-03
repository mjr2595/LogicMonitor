from __future__ import print_function
import time
import logicmonitor_sdk
from logicmonitor_sdk.rest import ApiException
from pprint import pprint


# Configure API key authorization: LMv1
configuration = logicmonitor_sdk.Configuration()
configuration.company = ''
configuration.access_id = ''
configuration.access_key = ''

# create an instance of the API class
api_instance = logicmonitor_sdk.LMApi(
    logicmonitor_sdk.ApiClient(configuration))

value = "true"

body = {
    "customProperties": [
        {
            "name": "alert",
            "value": value
        }
    ]
}

try:
    api_response = api_instance.patch_device(id=281, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DevicesApi->patchDevice: %s\n" % e)
