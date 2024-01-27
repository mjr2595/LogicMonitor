from __future__ import print_function
import os
import logicmonitor_sdk
from dotenv import load_dotenv
from logicmonitor_sdk.rest import ApiException
from pprint import pprint

load_dotenv()

# Configure API key authorization: LMv1
configuration = logicmonitor_sdk.Configuration()
configuration.company = os.getenv("PORTAL")
configuration.auth_type = 'Bearer'
configuration.bearer_token = os.getenv("BEARER")

# create an instance of the API class
api_instance = logicmonitor_sdk.LMApi(
    logicmonitor_sdk.ApiClient(configuration))

try:
    # get alert list
    api_response = api_instance.get_alert_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LMApi->getAlertList: %s\n" % e)
