import logicmonitor_sdk
import sys

creds = logicmonitor_sdk.Configuration()
creds.company = ''
creds.access_id = ''
creds.access_key = ''

api = logicmonitor_sdk.LMApi(logicmonitor_sdk.ApiClient(creds))

try:
   body = {"name":"Clients","parentId": 17}
   clientsGroup = api.add_device_group(body)
   print(f"Created parent clients group: {clientsGroup.id}")
except logicmonitor_sdk.rest.ApiException as e:
   print(f"Exception when calling LMApi->addDeviceGroup: {e}")
   print("Could not create parent group.")
   sys.exit()

try:
   clients = {
       "Acme":"startsWith(system.displayname,\"10.160.3.5\")",
       "Gold Standard Plumbing":"system.displayname == \"10.160.3.99\" or system.displayname == \"10.160.3.50\"",
       "Oklahoma Joe":"startsWith(system.displayname, \"SQL\")"
   }
   for client,appliesTo in clients.items():
       body = {"name":client, "parentId":clientsGroup.id, "appliesTo":appliesTo}
       clientGroup = api.add_device_group(body)
       print(f"Created group for {client}: {clientGroup.id}")
except logicmonitor_sdk.rest.ApiException as e:
   print(f"Exception when calling LMApi->addDeviceGroup: {e}")