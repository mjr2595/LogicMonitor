import logicmonitor_sdk
import sys
from logicmonitor_sdk.rest import ApiException

# Configure API key authorization: LMv1
creds = logicmonitor_sdk.Configuration()
creds.company = ''
creds.access_id = ''
creds.access_key = ''

# Create an instance of the API class
api = logicmonitor_sdk.LMApi(logicmonitor_sdk.ApiClient(creds))

# Create device group for these servers
try:
   body = {"name":"AppServers","parentId": 1}
   serverGroup = api.add_device_group(body)
   print(f"Created parent group for all appservers: {serverGroup.id}")
except logicmonitor_sdk.rest.ApiException as e:
   print(f"Exception when calling LMApi->addDeviceGroup: {e}")
   print("Could not create parent group.")
   sys.exit()

# Define server range
serverRangeStart = 1
serverRangeEnd = 90

# Loop through the range of servers
for x in range(serverRangeStart, serverRangeEnd+1):
   # Format to 2 digits
   serverNum = "{:02d}".format(x)
   # Concet server name
   serverName = "appserver" + serverNum + ".trainlm.com"
   # Construct body for request
   body = {"name": serverName,"displayName": serverName,"preferredCollectorId": 4, "hostGroupIds":serverGroup.id}

   try:
      # add device
      api_response = api.add_device(body)
      print("Added: " + serverName)
   except ApiException as e:
      print("Exception when calling LMApi->addDevice: %s\n" % e)
