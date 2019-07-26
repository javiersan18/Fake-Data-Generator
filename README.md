# Fake Data Generator 
## Apache Log Generator (Files)
## Fake Data Generator for Kafka / SQL

This script generates finite or infinite fake apache logs or fake Bank and Credit Card information (in this initial release) to send to Kafka or to insert in SQL tables (MySQL or PostgreSQL).
Its useful for generating fake data to test Big Data tools like Apache Flume, Apache Kafka, Apache Spark-Streaming and connecting all of them together.

It is easily extendible (both Data Generators and Outputs). Next versions will implement:
  - NoSQL output as MongoDB or DynamoDB.
  - Standard linux output.
  - Elegible type of fake data (Credit Cards, Purchase Transactions, Location data, etc.)


It is inspired (forked) by the work of [Fake-Apache-Log-Generator](https://github.com/kiritbasu/Fake-Apache-Log-Generator) and utilizes the [Faker](https://github.com/joke2k/faker/) library to generate realistic data. Feel free to fork it or contribute it in any way.

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
                        Log destination file path
  -n NUM_LINES, --number-lines NUM_LINES
                        Number of lines to generate (default: 10)
  -s SECONDS, --sleep-loop SECONDS
                        Write every SECONDS seconds. If SECONDS>0 it will
                        produce an infinite loop (default:0.0)
  -f {CLF,ELF}, --log-format {CLF,ELF}
                        Log format: Common or Extended Log Format (default:
                        ELF)
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

optional arguments:
  -h, --help            show this help message and exit
  -t KAFKA_TOPIC, --topic KAFKA_TOPIC
                        Kafka topic
  -n NUM_LINES, --number-lines NUM_LINES
                        Number of lines to generate (default: 10)
  -s SECONDS, --sleep-loop SECONDS
                        Write every SECONDS seconds. If SECONDS>0 it will
                        produce an infinite loop (default:0.0)

JSON file options:
  -p KAFKA_PROPS, --properties_file KAFKA_PROPS
                        JSON file with Kafka Producer properties

Command-line options:
  -b KAFKA_BROKERS, --brokers KAFKA_BROKERS
                        List of Kafka brokers
```

## Basic Usage for SQL generation

Infinite data generation using PostgreSQL(useful for testing Apache SQOOP or any other SQL analytics tools)
```
$ python apache-fake-log-gen.py sql -d postgres -sh localhost -db test_fake_gen -u test -pw TEst2019!
```

Infinite data generation using MySQL
```
$ python apache-fake-log-gen.py sql -d mysql -sh localhost -db test_fake_gen -u test -pw TEst2019!
```

Detailed help
```
$ python fake-data-gen.py sql -h
usage: fake-data-gen.py sql [-h] [-d SQL_DRIVER] -sh SQL_HOST [-p SQL_PORT]
                            -db SQL_DATABASE -u SQL_USERNAME -pw SQL_PASSWORD
                            [-n NUM_LINES] [-s SECONDS]

optional arguments:
  -h, --help            show this help message and exit
  -d SQL_DRIVER, --driver SQL_DRIVER
                        SQL database type ("mysql" or "postgres")
  -sh SQL_HOST, --host SQL_HOST
                        DB Host IP
  -p SQL_PORT, --port SQL_PORT
                        MySQL or PostgreSQL port. Needed only if different
                        than default ones
  -db SQL_DATABASE, --database SQL_DATABASE
                        MySQL or PostgreSQL database
  -u SQL_USERNAME, --username SQL_USERNAME
                        MySQL or PostgreSQL username
  -pw SQL_PASSWORD, --password SQL_PASSWORD
                        MySQL or PostgreSQL password
  -n NUM_LINES, --number-lines NUM_LINES
                        Number of lines to generate (default: 10)
  -s SECONDS, --sleep-loop SECONDS
                        Write every SECONDS seconds. If SECONDS>0 it will
                        produce an infinite loop (default:0.0)
```


## Requirements
* Python 3
* MySQL or PostgreSQL (>9.1) connectors if needed (mysql-connector-python / psycopg2)
* ```pip install -r requirements.txt```

## License
This script is released under the [Apache version 2](LICENSE) license.
