#!/usr/bin/env python3
import time, os, sys
import hmac, hashlib, base64
import requests
import json
import psutil

#--------------------------------------
# Constants - Do not change
#--------------------------------------
resource_path = '/metric/ingest'
headers =  {
	   'Content-Type': 'application/json'
	  }

#---------------------------------------
# Change Values below as per your setup
#---------------------------------------
def get_params():
	# Account info
	# Your account name

    AccessId =''
    AccessKey =''
    Company = ''

    url = "https://"+Company+".logicmonitor.com/rest"+ resource_path
    return url, AccessId, AccessKey


#--------------------------------------------
# Function to send metric data to LM Platform
#--------------------------------------------
def send_metrics(timestamp, body):
		url, AccessId, AccessKey  = get_params()
		req_var =  "POST" + str(timestamp) + body +resource_path;
		signature = base64.b64encode(bytes(hmac.new(
                            bytes(AccessKey, 'latin-1'),
                            bytes(req_var, 'latin-1'),
                            digestmod=hashlib.sha256
                        ).hexdigest(), 'latin-1')).decode('latin-1')
		auth = "LMv1 "+AccessId+ ":"+ signature+":"+str(timestamp)
		headers['Authorization'] =  auth
		try:
			response = requests.post(url, verify=True, headers=headers, data=body,  params={"create":'true'})
			if response.status_code != 202:
				print('Failed to send metric. Error:', response.status_code, response.text)
			else:
				print("SUCCESS :",response.text)
		except Exception as e:
			print("Unable to connect. Error: ", e)

#--------------------------------------------
# Prepare REST payload
#--------------------------------------------
def prepare_request_body(metric, timestamp, data_value):
	return json.dumps({
	    "resourceName": metric["device_name"],
	    "resourceIds": {
			"system.displayname": metric["device_name"],
			"system.ips": metric["device_ip"]
	    },
	    "dataSource": metric["data_source"],
	    "dataSourceDisplayName": metric["data_source"],
	    "instances": [
			{
				"instanceName": metric["instance"],
				"instanceDisplayName": metric["instance"],
				"instanceProperties": {
					"version": "1",
				},
				"dataPoints": [
					{
						"dataPointName": metric["data_point"],
						"dataPointType": "GAUGE",
						"dataPointAggregationType": "sum",
						"values": {
							str(timestamp//1000): data_value
						}
					},
		    	]
			},
	    ]
	}).replace("'", '"')


#------------------
#====  MAIN =======
#------------------
if __name__ == "__main__":
	my_metric = {}
	my_metric["device_name"] = os.uname()[1]
	my_metric["device_ip"] = "192.168.1.1"
	my_metric["data_source"] = "CPU"
	my_metric["instance"] = "cpu-1"
	my_metric["data_point"] = "cpu_utilization"
	while True:
		timestamp = int(time.time()*1000)
		data_value = psutil.cpu_percent()

		body = prepare_request_body(my_metric, timestamp, data_value)
		send_metrics(timestamp, body)
		time.sleep(10)