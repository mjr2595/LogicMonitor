import com.santaba.agent.groovyapi.snmp.Snmp;
 
//Getting the Hostname to be used
def hostname = hostProps.get("system.hostname");
//Get processes from property
def processesProp = hostProps.get("processes");
//cast as array of Strings
def processes = processesProp.split(",")

// Choose the oid to walk, need combo of both
def oid1 = "1.3.6.1.2.1.25.4.2.1.4";
def oid2 = "1.3.6.1.2.1.25.4.2.1.5";
 
// Walk both oids
def oidOneWalk = Snmp.walk(hostname, oid1);
def oidTwoWalk = Snmp.walk(hostname, oid2);

// combine all processes into single list
combinedWalk = oidOneWalk + oidTwoWalk
def list = combinedWalk.readLines();

// Make a map to store results in
def results = [:];
 
// Loop through the returned lines
list.each
{ line->
	 
	// Split the result
	tokens = line.split("=");

	// Check that the path has the processToMonitor in it
	processes.each
	{ process->
		if(tokens.last().toLowerCase().contains(process.toLowerCase()))
		{
			def result = results[tokens.last().split("/").last()];
		   
			// Check to see if this result isnt in the map
			if(result == null)
			{
				// Create a list for theoids to go in
			  result = [];
			}
			 // Add the oid to the list in the result
			result.add(tokens.first().split("\\.").last().trim());

			// Add this result to the Map
			results[tokens.last().split("/").last()] = result;
		}
	}
}


// Loop through all results
results.each
{
    key, value ->
   
    // Print the results in the standard AD format
    println(value.join(',') + "##" + key);
}
 
return 0;