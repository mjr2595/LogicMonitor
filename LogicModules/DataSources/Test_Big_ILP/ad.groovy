import com.logicmonitor.mod.Snippets
import com.santaba.agent.groovy.utils.GroovyScriptHelper as GSH

def modLoader = GSH.getInstance(GroovySystem.version).getScript("Snippets", Snippets.getLoader()).withBinding(getBinding())
def emit = modLoader.load("lm.emit", "0")

def ilp = [
        "auto.a": randomString(10),
        "auto.b": randomString(10),
        "auto.c": randomString(48980)
]

//def ilp1 = randomString(24500)
//def ilp2 = randomString(24500)
//def ilp3 = randomString(16500)

def ilp_truncated = emit.truncateToLimit(ilp)

for (int i = 1; i <= 4; i++) {
    def wildvalue = "instance${i}_value"
    def wildalias = "instance${i}_alias"
    def description = "instance${i}_description"
    emit.instance(wildvalue, wildalias, description, ilp_truncated)
    //println("${wildvalue}##${wildalias}##${description}####a=${ilp1}&b=${ilp2}")
    //println("${wildvalue}##${wildalias}##${description}####a=${ilp1}&b=${ilp2}&c=${ilp3}")
}

String randomString(int length) {
    String prefix = String.valueOf(length)
    int prefixLen = prefix.length()

    if (length < prefixLen) {
        throw new IllegalArgumentException("Length must be at least ${prefixLen} to include its own value as prefix.")
    }

    int remaining = length - prefixLen
    final String chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    final Random random = new Random()
    final StringBuilder sb = new StringBuilder(length)
    sb.append(prefix)
    for (int i = 0; i < remaining; i++) {
        sb.append(chars.charAt(random.nextInt(chars.length())))
    }
    return sb.toString()
}
