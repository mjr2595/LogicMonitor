// datapoint1
println "instance1_value.key1=11"
println "instance2_value.key1=21"
println "instance3_value.key1=31"
println "instance4_value.key1=41"

// datapoint2
println "instance1_value.key2=12"
println "instance2_value.key2=22"
println "instance3_value.key2=32"
println "instance4_value.key2=42"

// JSON equivalent
/*
{
  data: {
    instance1_value: {
      values: {
        "key1": 11,
        "key2": 12
      }
    },
    instance2_value: {
      values: {
        "key1": 21,
        "key2": 22
      }
    },
    instance3_value: {
      values: {
        "key1": 31,
        "key2": 32
      }
    },
    instance4_value: {
      values: {
        "key1": 41,
        "key2": 42
      }
    }
  }
}
*/