import com.santaba.agent.groovyapi.expect.Expect;
 
hostname = hostProps.get("system.hostname");
userid = hostProps.get("ssh.user");
passwd = hostProps.get("ssh.pass");
port = hostProps.get("ssh.port") ?: "22"
lib = "jsch"
 
useSSHJ = false // Change this to true to test SSHJ.
 
if(useSSHJ) {
    lib = "sshj"
}
 
// timeout
timeout = 10
 
// initiate an ssh connection to the host using the provided credentials
ssh_connection = Expect.open(hostname, port.toInteger(), userid, passwd, timeout,"lib=${lib}");
 
sleep(1000);
 
// send a command
ssh_connection.send('show ?\n');
 
sleep(1000);
 
// print the output output
println "stdout " + ssh_connection.stdout();
 
// Logout
ssh_connection.send('exit\n')
 
// close the ssh connection handle then print the config
ssh_connection.expectClose();
return 0;