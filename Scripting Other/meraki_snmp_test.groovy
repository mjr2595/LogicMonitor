import com.santaba.agent.groovyapi.snmp.Snmp;

def community = hostProps.get("snmp.community");
def port = 16100;
def version = hostProps.get("snmp.version");

def oid = "1.3.6.1.4.1.29671.1.1.4.1.3";

def s_walk_out = Snmp.walk('snmp.meraki.com',community, version, oid, 15000, port);
def list = s_walk_out.readLines();
list.each{ value ->
	println value
}

return 0;
