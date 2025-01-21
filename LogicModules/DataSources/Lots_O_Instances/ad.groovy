def count = hostProps.get("instances.amount").toInteger()

for (int i = 1; i <= count; i++) {
    println "instance${i}_value##instance${i}_alias"
}