import com.santaba.agent.groovyapi.expect.Expect;
import com.santaba.agent.util.Settings
 
def hostname = hostProps.get("system.hostname")
def user = hostProps.get("ssh.user")
def pass = hostProps.get("ssh.pass")
def port = hostProps.get("ssh.port", "22").toInteger()
def timeout = hostProps.get("ssh.timeout") ?: Settings.getGroovyExpectTimeoutInSecond() ?: 10
def lib = "sshj"

useJSCH = false // Change this to true to test the older JSCH

if (useJSCH) {
    lib = "jsch"
}

// open the ssh connection
def cli = Expect.open(hostname, port, nimuser, nimpass, timeout, "lib=${lib}")

sleep(1000)

// send a command, just newline to get the prompt
cli.send('\n\r')

sleep(1000)

println "stdout:\n" + cli.stdout()

// logout
cli.send('exit\n')

// close the ssh connection
cli.expectClose()
return 0