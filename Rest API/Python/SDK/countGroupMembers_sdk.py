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

api = logicmonitor_sdk.LMApi(logicmonitor_sdk.ApiClient(configuration))

try:
    fields = "id,name"
    filter = "name:\"Sites\""
    parentGroupId = api.get_device_group_list(
        fields=fields, filter=filter).items[0].id

except logicmonitor_sdk.rest.ApiException as e:
    print("Could not find the parent group.")
    print(f"Exception when calling LMApi->getDeviceGroupList: {e}")

try:
    filter = f"parentId:{parentGroupId}"
    childGroups = api.get_device_group_list(filter=filter).items
    for group in childGroups:
        print(f"{group.name}: {group.num_of_direct_devices}")

except logicmonitor_sdk.rest.ApiException as e:
    print("Could not fetch the child groups.")
    print(f"Exception when calling LMApi->getDeviceGroupList: {e}")
