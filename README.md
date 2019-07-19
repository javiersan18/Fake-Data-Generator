# Fake Apache Log Generator (File) and Fake Data Generator for Kafka

This script generates finite or infinite fake apache logs or fake Bank and Credit Card information to send to Kafka.
Its useful for generating fake data to test Big Data tools like Apache Flume, Apache Kafka, Apache Spark-Streaming and connecting all of them together.


It is inspired (fork) by the work of [Fake-Apache-Log-Generator](https://github.com/kiritbasu/Fake-Apache-Log-Generator) and utilizes the library [Faker](https://github.com/joke2k/faker/) library to generate realistic data.

***

## Basic Usage for LOG generation

Generate 100 log lines into a .log file in the current directory
```
$ python fake-data-gen.py -n 100
```

Infinite log file generation (useful for testing Apache Flume applications)
```
$ python apache-fake-log-gen.py -n 100 -s 1
```

Detailed help
```
$ python fake-data-gen.py log -h
usage: fake-data-gen.py log [-h] -o LOG_FILE_PATH [-n NUM_LINES] [-s SECONDS]
                            [-f {CLF,ELF}]

optional arguments:
  -h, --help            show this help message and exit
  -o LOG_FILE_PATH, --output-path LOG_FILE_PATH
                        Log path
  -n NUM_LINES, --number-lines NUM_LINES
                        Number of lines to generate (default: 10)
  -s SECONDS, --sleep-loop SECONDS
                        Write every SECONDS seconds. If SECONDS>0 infinite
                        loop (default:0.0)
  -f {CLF,ELF}, --log-format {CLF,ELF}
                        Log format, Common or Extended Log Format

```

## Basic Usage for KAFKA generation

Infinite data generation (useful for testing Apache Kafka and streaming applications (Apache Spark, Apache Flink, KSQL, etc.))
```
$ python apache-fake-log-gen.py kafka -t testTopic -b localhost:9092 -n 100 -s 1
```

Generate 100 lines and send them to kafka brokers. (Advanced Kafka configuration in JSON file)
```
$ python apache-fake-log-gen.py kafka -t testTopic -p kafka_properties.json -n 100
```

Detailed help
```
$ python fake-data-gen.py kafka -h
usage: fake-data-gen.py kafka [-h] -t KAFKA_TOPIC [-n NUM_LINES] [-s SECONDS]
                              [-p KAFKA_PROPS] [-b KAFKA_BROKERS]
                              [-sr KAFKA_SCHEMA_REGISTRY]

optional arguments:
  -h, --help            show this help message and exit
  -t KAFKA_TOPIC, --topic KAFKA_TOPIC
                        Kafka topic
  -n NUM_LINES, --number-lines NUM_LINES
                        Number of lines to generate (default: 10)
  -s SECONDS, --sleep-loop SECONDS
                        Write every SECONDS seconds. If SECONDS>0 infinite
                        loop (default:0.0)

JSON file options:
  -p KAFKA_PROPS, --properties_file KAFKA_PROPS
                        JSON file with Kafka Producer properties.

Command-line options:
  -b KAFKA_BROKERS, --brokers KAFKA_BROKERS
                        List of Kafka brokers
  -sr KAFKA_SCHEMA_REGISTRY, --schema-registry KAFKA_SCHEMA_REGISTRY
                        URL to Schema-Registry
```



## Requirements
* Python 3
* ```pip install -r requirements.txt```

## License
This script is released under the [Apache version 2](LICENSE) license.
