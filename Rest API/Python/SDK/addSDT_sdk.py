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
    
body = {
  "id" : "S_9",
  "admin" : "",
  "startDateTime" : 1672780800,
  "endDateTime" : 1672783560000,
  "isEffective" : True,
  "timezone" : "America/Chicago",
  "type" : "WebsiteSDT",
  "sdtType" : "oneTime",
  "weekDay" : "Sunday",
  "websiteId" : 16,
  "websiteName" : "webcheck"
}

try:
    # add SDT (Response may contain extra fields depending upon the type of SDT being added)
    api_response = api_instance.add_sdt(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SDTsApi->addSDT: %s\n" % e)