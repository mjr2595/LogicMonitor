import org.apache.commons.codec.binary.Hex
import org.apache.http.client.methods.HttpPost
import org.apache.http.entity.ContentType
import org.apache.http.entity.StringEntity
import org.apache.http.impl.client.CloseableHttpClient
import org.apache.http.impl.client.HttpClients
import org.apache.http.util.EntityUtils
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec

def debug = true

//define credentials and url
def accessId = hostProps.get('lmaccess.id') ?: hostProps.get('logicmonitor.access.id')
def accessKey = hostProps.get('lmaccess.key') ?: hostProps.get('logicmonitor.access.key')
def account = hostProps.get('lmaccount') ?: Settings.getSetting(Settings.AGENT_COMPANY)
def deviceId = hostProps.get('system.deviceId')

def resourcePath = '/log/ingest'
def url = 'https://' + account + '.logicmonitor.com/rest' + resourcePath

def data = """
[
  {
    "msg": "Test Ingest from DS",
    "_lm.resourceId": {
      "system.deviceId": "${deviceId}"
    }
  }
]
"""

StringEntity params = new StringEntity(data, ContentType.APPLICATION_JSON)
epoch = System.currentTimeMillis()
requestVars = 'POST' + epoch + data + resourcePath

// construct signature
hmac = Mac.getInstance('HmacSHA256')
secret = new SecretKeySpec(accessKey.getBytes(), 'HmacSHA256')
hmac.init(secret)
hmac_signed = Hex.encodeHexString(hmac.doFinal(requestVars.getBytes()))
signature = hmac_signed.bytes.encodeBase64()

// HTTP Post
CloseableHttpClient httpclient = HttpClients.createDefault()
http_request = new HttpPost(url)
http_request.setHeader('Authorization', 'LMv1 ' + accessId + ':' + signature + ':' + epoch)
http_request.setHeader('Accept', 'application/json')
http_request.setHeader('Content-type', 'application/json')
http_request.setHeader('X-version', '3')
http_request.setEntity(params)
response = httpclient.execute(http_request)
responseBody = EntityUtils.toString(response.getEntity())
code = response.getStatusLine().getStatusCode()

// Debug Info
if (debug) {
  println 'Signature: ' + signature
  println 'URL: ' + url
  println 'Data: ' + data
  println 'Response: ' + responseBody
  println 'Status: ' + code
}

httpclient.close()

return code == 202 ? 0 : 1
