def command = "ls /path/to/directory" // Replace with your desired command
def proc = command.execute()

// Capture standard output and error streams
def outputStream = new StringBuilder()
proc.waitForProcessOutput(outputStream, System.err)

// Print the output
println "Standard Output:\n${outputStream.toString()}"

// Check for errors
if (proc.exitValue() != 0) {
    println "Error occurred. Exit code: ${proc.exitValue()}"
}
