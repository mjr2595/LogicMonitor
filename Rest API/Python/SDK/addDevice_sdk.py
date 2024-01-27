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
api_instance = logicmonitor_sdk.LMApi(logicmonitor_sdk.ApiClient(configuration))
body = {"name": "1.1.1.1","displayName": "myOtherDevice","preferredCollectorId": 8,"disableAlerting": "true"}

try:
    # add device
    api_response = api_instance.add_device(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LMApi->addDevice: %s\n" % e)