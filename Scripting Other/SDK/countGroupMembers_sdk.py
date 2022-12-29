import logicmonitor_sdk
import sys

creds = logicmonitor_sdk.Configuration()
creds.company = ''
creds.access_id = ''
creds.access_key = ''

api = logicmonitor_sdk.LMApi(logicmonitor_sdk.ApiClient(creds))

try:
   fields = "id,name"
   filter = "name:\"Clients\""
   parentGroupId = api.get_device_group_list(fields=fields, filter=filter).items[0].id

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