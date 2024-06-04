import groovy.time.*

hostname = hostProps.get("system.hostname");
ports = 80

def startTime = new Date()

ports.each { port ->
try {
  Socket socket = new Socket(hostname,port)
  println("Port ${port}: OPEN")
} catch (e) {
  println("Port ${port}: CLOSED")
  }
}
def endTime = new Date()
TimeDuration duration = TimeCategory.minus(endTime, startTime)

println ""
println "It took ${duration} to test the port.."