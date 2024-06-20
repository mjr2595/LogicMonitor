/* 
Script to contruct the auth header for the LM API
Should be added within Postman as a pre-request script
LM community post with steps: 
https://community.logicmonitor.com/discussions/product-discussions/accessing-the-logicmonitor-rest-api-with-postman-and-lmv1-api-token-authenticati/5143?topicRepliesSort=postTimeDesc

Note: this script is not needed if using bearer token auth
*/

var btoa = require("btoa");
var cjs = require("crypto-js");

// Get API credentials from environment variables
var api_id = pm.environment.get("api_id");
var api_key = pm.environment.get("api_key");

// Get the HTTP method from the request
var http_verb = pm.request.method;

// Extract the resource path from the request URL
var resource_path = pm.request.url
  .toString()
  .replace(/(^{{url}})([^\?]+)(\?.*)?/, "$2");

// Get the current time in epoch format
var epoch = new Date().getTime();

// If the request includes a payload, included it in the request variables
var request_vars =
  http_verb == "GET" || http_verb == "DELETE"
    ? http_verb + epoch + resource_path
    : http_verb + epoch + pm.request.body + resource_path;

// Generate the signature and build the Auth header
var signature = btoa(cjs.HmacSHA256(request_vars, api_key).toString());
var auth = "LMv1 " + api_id + ":" + signature + ":" + epoch;

// Write the Auth header to the environment variable
pm.environment.set("auth", auth);
