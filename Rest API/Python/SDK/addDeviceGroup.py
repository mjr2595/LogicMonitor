from __future__ import print_function
import time
import logicmonitor_sdk
from logicmonitor_sdk.rest import ApiException
from pprint import pprint


# Configure API key authorization: LMv1
configuration = logicmonitor_sdk.Configuration()
configuration.company = 'YOUR_COMPANY'
configuration.access_id = 'YOUR_ACCESS_ID'
configuration.access_key = 'YOUR_ACCESS_KEY'

# create an instance of the API class
api_instance = logicmonitor_sdk.LMApi(logicmonitor_sdk.ApiClient(configuration))
    
body = swagger_client.models.DeviceGroup(
    full_path=,# String
    group_type=,# String | example: "Normal"
    num_of_aws_devices=,# Integer
    description=,# String | example: "Linux Servers"
    applies_to=,# String | example: "isLinux()"
    gcp_test_result_code=,# Integer
    disable_alerting=,# Boolean | example: True
    aws_regions_info=,# String
    created_on=,# Integer
    has_netflow_enabled_devices=,# Boolean
    num_of_azure_devices=,# Integer
    default_collector_description=,# String
    default_collector_id=,# Integer | example: 1.0
    aws_test_result=,# Object
    extra=,# Object
    num_of_direct_sub_groups=,# Integer
    sub_groups=,# Array
    num_of_direct_devices=,# Integer
    id=,# Integer
    enable_netflow=,# Object | example: true
    azure_test_result_code=,# Integer
    effective_alert_enabled=,# Boolean
    user_permission=,# String
    gcp_regions_info=,# String
    group_status=,# String
    num_of_gcp_devices=,# Integer
    azure_test_result=,# Object
    parent_id=,# Integer | example: 1.0
    aws_test_result_code=,# Integer
    custom_properties=,# Array
    num_of_hosts=,# Integer
    name=,# String | example: "Linux Servers"
    gcp_test_result=,# Object
    azure_regions_info=,# String
)

try:
    # add device group
    api_response = api_instance.add_device_group(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LMApi->addDeviceGroup: %s\n" % e)