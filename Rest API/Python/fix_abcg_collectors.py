#!/usr/bin/python

import requests

# Account Info
portal = ''
bearer = ''
auth = 'bearer ' + bearer
headers = {'Content-Type': 'application/json',
           'X-version': '3', 'Authorization': auth}


def main():
    # Get list of auto-balanced collector group ids
    path = '/setting/collector/groups'
    params = '?filter=autoBalance:true'
    abcg_id_list = get_abcg_ids(path, params)

    if abcg_id_list is not None:
        # For each aabcg id, get the list of devices in that group
        # For each device, set autoBalancedCollectorGroupId to preferredCollectorGroupId
        path = '/device/devices'
        params = '?filter=autoBalancedCollectorGroupId:0,preferredCollectorGroupId:'
        for abcg_id in abcg_id_list:
            print("Fixing ABCG " + str(abcg_id))
            fix_resource_collectors(path, params, abcg_id)
    else:
        print("No ABCG IDs found.")


def get_abcg_ids(path, params):
    try:
        url = 'https://' + portal + '.logicmonitor.com/santaba/rest' + path + params
        response = requests.get(url, headers=headers, verify=True)
        # Raises stored HTTPError, if one occurred.
        response.raise_for_status()
        response_json = response.json()
        id_list = [item['id'] for item in response_json['items']]
        return id_list
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def fix_resource_collectors(path, params, abcg_id):
    try:
        abcg_id = str(abcg_id)
        url = 'https://' + portal + '.logicmonitor.com/santaba/rest' + \
            path + params + abcg_id
        response = requests.get(url, headers=headers, verify=True)
        # Raises stored HTTPError, if one occurred.
        response.raise_for_status()
        response_json = response.json()
        for device in response_json['items']:
            device_id = str(device['id'])
            print("Updating deviceID " + device_id)
            url = 'https://' + portal + \
                '.logicmonitor.com/santaba/rest' + path + '/' + device_id
            data = '{"autoBalancedCollectorGroupId":' + abcg_id + '}'
            requests.patch(url, data=data, headers=headers, verify=True)
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


if __name__ == "__main__":
    main()
