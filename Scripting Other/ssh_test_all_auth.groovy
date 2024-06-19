import com.jcraft.jsch.JSch
import com.jcraft.jsch.Session
import com.jcraft.jsch.ChannelExec
import com.santaba.agent.groovyapi.expect.Expect
import java.io.ByteArrayOutputStream
import net.schmizz.sshj.SSHClient
import net.schmizz.sshj.userauth.keyprovider.KeyProvider
import net.schmizz.sshj.transport.verification.PromiscuousVerifier
   
// Setup connection properties
hostname = hostProps.get("system.hostname")
userid = hostProps.get("ssh.user")
passwd = hostProps.get("ssh.pass")
port = hostProps.get("ssh.port") ?: "22"
cert = hostProps.get("ssh.cert") ?: '~/.ssh/id_rsa'
lib = "jsch"
   
useSSHJ = false // Change this to true to test sshj
   
timeout = 10000

//Here is where you pass any terminal command relevant to the targeted device 
String command = 'show version'
String output
  
// The main conditional logic where the appropriate function is called based on the conditions
if (useSSHJ) {
    if (passwd) {
        println "Sending command via password authentication with SSHJ: $command"
        output = sshConnectionWithPasswordSSHJ(command)
    } else {
        println "Sending command via certificate authentication with SSHJ: $command"
        output = sshConnectionWithCertSSHJ(command)
    }
} else {
    if (passwd) {
        println "Sending command via password authentication with JSch: $command"
        output = sshConnectionWithPasswordJSch(command) // Call the new method here
    } else {
        println "Sending command via certificate authentication with JSch: $command"
        output = sshConnectionWithCertJSch(command)
    }
}
   
def sshConnectionWithPasswordSSHJ(String command) {
    SSHClient ssh = new SSHClient()
    ssh.addHostKeyVerifier(new PromiscuousVerifier())
   
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream()
   
    try {
        ssh.connect(hostname, port.toInteger())
        ssh.authPassword(userid, passwd)
        println "SSHJ session established with password authentication."
   
        def session = ssh.startSession()
        try {
            def cmd = session.exec(command)
            cmd.join()
               
            byte[] buffer = new byte[1024]
            int read
            while ((read = cmd.getInputStream().read(buffer)) != -1) {
                outputStream.write(buffer, 0, read)
            }
            println "Command execution completed with SSHJ using password."
        } finally {
            session.close()
        }
    } finally {
        ssh.disconnect()
    }
    String output = outputStream.toString()
    println "stdout: \n$output"
    return output
}
   
def sshConnectionWithCertSSHJ(String command) {
    SSHClient ssh = new SSHClient()
    ssh.addHostKeyVerifier(new PromiscuousVerifier())
   
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream()
   
    try {
        ssh.connect(hostname, port.toInteger())
        ssh.authPublickey(userid, ssh.loadKeys(cert))
        println "SSHJ session established with certificate authentication."
   
        def session = ssh.startSession()
        try {
            def cmd = session.exec(command)
            cmd.join()
               
            byte[] buffer = new byte[1024]
            int read
            while ((read = cmd.getInputStream().read(buffer)) != -1) {
                outputStream.write(buffer, 0, read)
            }
            println "Command execution completed with SSHJ using certificate."
        } finally {
            session.close()
        }
    } finally {
        ssh.disconnect()
    }
    String output = outputStream.toString()
    println "stdout: \n$output" // Ensuring consistency in output printing
    return output
}
   
def sshConnectionWithPasswordJSch(String command) {
    JSch jsch = new JSch()
    Session session = jsch.getSession(userid, hostname, port.toInteger())
    session.setPassword(passwd)
    session.setConfig("StrictHostKeyChecking", "no")
    session.setTimeout(timeout)
    session.connect()
    println "SSH session established with JSch using password authentication."
  
    ChannelExec channel = (ChannelExec) session.openChannel("exec")
    channel.setCommand(command)
  
    channel.setInputStream(null)
  
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream()
    ByteArrayOutputStream errorStream = new ByteArrayOutputStream()
  
    channel.setOutputStream(outputStream)
    channel.setErrStream(errorStream)
  
    channel.connect()
  
    while (!channel.isClosed()) {
        Thread.sleep(100)
    }
      
    println "Command execution completed with JSch using password."
    String output = outputStream.toString()
    String error = errorStream.toString()
  
    channel.disconnect()
    session.disconnect()
    println "SSH session disconnected with JSch using password."
  
    if (!error.isEmpty()) {
        println "stderr: \n$error"
    }
  
    println "stdout: \n$output"
    return output
}
 
 
def sshConnectionWithCertJSch(String command) {
    JSch jsch = new JSch()
    jsch.addIdentity(cert)  // Load the certificate
    Session session = jsch.getSession(userid, hostname, port.toInteger())
    session.setConfig("StrictHostKeyChecking", "no")
    session.setTimeout(timeout)
    session.connect()
    println "SSH session established with JSch using certificate authentication."
 
    ChannelExec channel = (ChannelExec) session.openChannel("exec")
    channel.setCommand(command)
 
    channel.setInputStream(null)
 
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream()
    ByteArrayOutputStream errorStream = new ByteArrayOutputStream()
 
    channel.setOutputStream(outputStream)
    channel.setErrStream(errorStream)
 
    channel.connect()
 
    while (!channel.isClosed()) {
        Thread.sleep(100)
    }
 
    println "Command execution completed with JSch using certificate."
    String output = outputStream.toString()
    String error = errorStream.toString()
 
    channel.disconnect()
    session.disconnect()
    println "SSH session disconnected with JSch using certificate."
 
    if (!error.isEmpty()) {
        println "stderr: \n$error"
    }
 
    println "stdout: \n$output"
    return output
}
   
return 0