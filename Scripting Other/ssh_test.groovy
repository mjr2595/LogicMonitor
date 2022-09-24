import com.santaba.agent.groovyapi.expect.Expect;

// get the hostname and credentials from the device property table
hostname = hostProps.get("system.hostname");
userid = hostProps.get("ssh.user");
passwd = hostProps.get("ssh.pass");

// initiate an ssh connection to the host using the provided credentials
ssh_connection = Expect.open(hostname, userid, passwd);

// wait for the cli prompt, which indicates we've connected
sleep(2000);
println "stdout " + ssh_connection.stdout();
// Logout
ssh_connection.send('exit\n')

// close the ssh connection handle then print the config
ssh_connection.expectClose();
return 0;