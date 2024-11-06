import com.logicmonitor.mod.Snippets
import com.santaba.agent.groovy.utils.GroovyScriptHelper as GSH
import groovy.json.JsonSlurper

def debug = false

def modLoader = GSH.getInstance(GroovySystem.version).getScript("Snippets", Snippets.getLoader()).withBinding(getBinding())
def emit = modLoader.load("lm.emit", "0")
def lmDebugSnip = modLoader.load("lm.debug", "1")
def lmDebug = lmDebugSnip.debugSnippetFactory(out, debug)
def httpSnip = modLoader.load("proto.http", "0")
def http = httpSnip.httpSnippetFactory(hostProps)

def url = "https://public.api.bsky.app"
def endpoint = "/xrpc/app.bsky.actor.getProfile"
def wild = instanceProps.get("wildvalue")
def params = [
        actor: wild
]

try {
    def response = http.rawGet(url + endpoint, null, params)
    def json = new JsonSlurper().parseText(response.inputStream.getText())
    json.each { key, value -> lmDebug.LMDebugPrint("$key: $value")}
    emit.dp("followersCount", json.followersCount)
    emit.dp("followsCount", json.followsCount)
    emit.dp("postsCount", json.postsCount)
    return 0
} catch (Exception e) {
    lmDebug.LMDebugPrint("Error: ${e.message}")
    return 1
}