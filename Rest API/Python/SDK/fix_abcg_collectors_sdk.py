from __future__ import print_function
import os
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


def main():
    # Get list of auto-balanced collector group ids
    abcg_id_list = get_abcg_ids()

    if abcg_id_list is not None:
        # For each aabcg id, get the list of devices in that group
        # For each device, set autoBalancedCollectorGroupId to preferredCollectorGroupId
        for abcg_id in abcg_id_list:
            print("Fixing ABCG " + str(abcg_id))
            fix_resource_collectors(abcg_id)
    else:
        print("No ABCG IDs found.")


def get_abcg_ids():
    try:
        response = api_instance.get_collector_group_list(
            filter='autoBalance:true')
        id_list = [item.id for item in response.items]
        return id_list
    except ApiException as e:
        print("Exception when calling CollectorGroupsApi->getCollectorGroupList: %s\n" % e)


def fix_resource_collectors(abcg_id):
    try:
        filter = 'autoBalancedCollectorGroupId:0,preferredCollectorGroupId:' + \
            str(abcg_id)
        response = api_instance.get_device_list(filter=filter)
        for device in response.items:
            device_id = device.id
            print("Updating deviceID " + str(device_id))
            body = {"autoBalancedCollectorGroupId": abcg_id}
            api_instance.patch_device(id=device_id, body=body)
    except ApiException as e:
        print(
            "Exception when calling DevicesApi: %s\n" % e)


if __name__ == "__main__":
    main()
