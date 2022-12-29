from __future__ import print_function
import time
# import swagger_client
# import swagger_client.models as models
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

id = 1558
# fields = fields_example

try:
    # get widget by id
    api_response = api_instance.get_widget_by_id(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LMApi->getWidgetById: %s\n" % e)