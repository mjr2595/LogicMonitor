import com.santaba.agent.groovyapi.snmp.Snmp;
 
//Get the Wildvalue and  Hostname
def hostname = "##HOSTNAME##";
def wildvalue = "##WILDVALUE##";
 
 // Split out oids back up from the list we sent them in via the AD script
def wildvalues = wildvalue.split(",");
 
// Make some counters to join the info from many datasources
def cpu = 0;
def mem = 0;
def status = 10;
def processes = wildvalues.length;

// Loop through each oid
wildvalues.each
{
    value ->

    // Walk the oids we need data from, and add them to our counters
    cpu += Snmp.get(hostname, ".1.3.6.1.2.1.25.5.1.1.1." + value).toInteger();
    mem += Snmp.get(hostname, ".1.3.6.1.2.1.25.5.1.1.2." + value).toInteger();
    status = Math.min(status, Snmp.get(hostname, ".1.3.6.1.2.1.25.4.2.1.7." + value).toInteger());
}

// Print off the counters so our datapoints can pick them up
println("CPU=" + cpu);
println("Memory=" + mem);
println("MatchingProcesses=" + processes);
println("MinStatus=" + status);