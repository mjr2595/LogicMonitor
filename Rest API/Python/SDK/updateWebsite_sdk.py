from __future__ import print_function

import os
from pprint import pprint

import logicmonitor_sdk
from dotenv import load_dotenv
from logicmonitor_sdk.rest import ApiException

load_dotenv()

# Configure API key authorization: LMv1
configuration = logicmonitor_sdk.Configuration()
configuration.company = os.getenv("PORTAL")
configuration.auth_type = 'Bearer'
configuration.bearer_token = os.getenv("BEARER")

# create an instance of the API class
api_instance = logicmonitor_sdk.LMApi(
    logicmonitor_sdk.ApiClient(configuration))

id = 19  # Integer | The id of the website to update
opType = "refresh"  # String |  (optional) (default to refresh)

body = logicmonitor_sdk.models.Website(
    name="Dev Portfolio",
    type="webcheck",
    test_location={
        "smgIds": [2, 3, 4, 5, 6],
        "collectorIds": [],
        "all": True,
        "collectors": []
    },
    properties=[{
        "name": "api",
        "value": "prop"
    }, {
        "name": "anotha",
        "value": "1"
    }]
)

try:
    # update website
    api_response = api_instance.patch_website_by_id(id, body, op_type=opType)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WebsitesApi->patch_website_by_id: %s\n" % e)
