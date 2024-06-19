/* 
Script to contruct the auth header for the LM API
Should be added within Postman as a pre-request script
LM community post with steps: 
https://community.logicmonitor.com/discussions/product-discussions/accessing-the-logicmonitor-rest-api-with-postman-and-lmv1-api-token-authenticati/5143?topicRepliesSort=postTimeDesc

Note: this script is not needed if using bearer token auth
*/

var btoa = require("btoa");
var cjs = require("crypto-js");

var api_id = pm.environment.get("api_id");
var api_key = pm.environment.get("api_key");

var http_verb = pm.request.method;
var resource_path = pm.request.url
  .toString()
  .replace(/(^{{url}})([^\?]+)(\?.*)?/, "$2");
var epoch = new Date().getTime();

var request_vars =
  http_verb == "GET" || http_verb == "DELETE"
    ? http_verb + epoch + resource_path
    : http_verb + epoch + pm.request.data + resource_path;

var signature = btoa(cjs.HmacSHA256(request_vars, api_key).toString());
var auth = "LMv1 " + api_id + ":" + signature + ":" + epoch;

pm.environment.set("auth", auth);
