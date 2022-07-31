from __future__ import print_function
import time
import logicmonitor_sdk
from logicmonitor_sdk.rest import ApiException
from pprint import pprint


# Configure API key authorization: LMv1
configuration = logicmonitor_sdk.Configuration()
configuration.company = 'COMPANY_NAME'
configuration.access_id = 'API_ACCESS_ID'
configuration.access_key = 'API_ACCESS_KEY'

# create an instance of the API class
api_instance = logicmonitor_sdk.LMApi(logicmonitor_sdk.ApiClient(configuration))

try:
    # get alert list
    api_response = api_instance.get_alert_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LMApi->getAlertList: %s\n" % e)