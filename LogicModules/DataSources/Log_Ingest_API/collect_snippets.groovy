import com.logicmonitor.common.sse.utils.GroovyScriptHelper as GSH
import com.logicmonitor.mod.Snippets
import org.apache.commons.codec.binary.Hex
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec

def debug = false

def modLoader = GSH.getInstance()._getScript('Snippets', Snippets.getLoader()).withBinding(getBinding())
def httpSnippet = modLoader.load('proto.http', '0').httpSnippetFactory(hostProps)

def apiId = hostProps.get('lmaccess.id') ?: hostProps.get('logicmonitor.access.id')
def apiKey = hostProps.get('lmaccess.key') ?: hostProps.get('logicmonitor.access.key')
def portalName = hostProps.get('lmaccount') ?: Settings.getSetting(Settings.AGENT_COMPANY)
def deviceId = hostProps.get('system.deviceId')
def url = 'https://' + portalName + '.logicmonitor.com/rest'
def resourcePath = 'log/ingest'

def log = """
[
  {
    "msg": "Test Ingest from DS snippet",
    "_lm.resourceId": {
      "system.deviceId": "${deviceId}"
    }
  }
]
"""

def auth = generateAuth(apiId, apiKey, log, resourcePath)
Map headers = ['Authorization': auth, 'Content-Type': 'application/json', 'X-version': '3']

def status = httpSnippet.rawPost("${url}/${resourcePath}", headers, log)

if (debug) {
  println "URL: ${url}/${resourcePath}"
  println "Data: ${log}"
  println "Status: ${status}"
  println "Response: ${status.content?.text}"
}

return status.responseCode == 202 ? 0 : 1

static String generateAuth(id, key, data, path) {
  Long epochTime = System.currentTimeMillis()
  Mac hmac = Mac.getInstance('HmacSHA256')
  hmac.init(new SecretKeySpec(key.getBytes(), 'HmacSHA256'))
  def digest = hmac.doFinal("POST${epochTime}${data}/${path}".getBytes())
  def signature = Hex.encodeHexString(digest).bytes.encodeBase64()
  return "LMv1 ${id}:${signature}:${epochTime}"
}
