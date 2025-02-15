#!/usr/bin/python
import os
import time
import argparse
from kafka.producer import Producer
from sql.sql_conn import SQLConnector
from generator.data_generator import DataGenerator


def main():
    parser = argparse.ArgumentParser(description='Fake data generator')
    subparsers = parser.add_subparsers(help='Data destination')

    # Logs commands
    log_parser = subparsers.add_parser('log', help='Generate Apache Logs')
    log_parser.add_argument('-o', '--output-path', required=True, dest='log_file_path', action='store', type=str,
                            help='Log destination file path')
    log_parser.add_argument('-of', '--output-file', required=False, dest='log_file_name', action='store', type=str,
                            help='If indicated, log file will be created with this name, otherwise will be auto generated')
    log_parser.add_argument('-n', '--number-lines', dest='num_lines', type=int, default=10, action='store',
                            help='Number of lines to generate (default: 10)')
    log_parser.add_argument('-s', '--sleep-loop', dest='seconds', type=float, default=0.0, action='store',
                            help='Write every SECONDS seconds. If SECONDS>0 it will produce an infinite loop (default:0.0)')
    log_parser.add_argument('-f', '--log-format', dest='log_format',
                            help='Log format: Common or Extended Log Format (default: ELF)',
                            choices=['CLF', 'ELF'], default='ELF')

    # Kafka commands
    kafka_parser = subparsers.add_parser('kafka', help='Send to Apache Kafka')
    kafka_parser.add_argument('-t', '--topic', required=True, dest='kafka_topic', action='store', help='Kafka topic')
    kafka_parser.add_argument('-n', '--number-lines', dest='num_lines', type=int, default=10, action='store',
                              help='Number of lines to generate (default: 10)')
    kafka_parser.add_argument('-s', '--sleep-loop', dest='seconds', type=float, default=0.0, action='store',
                              help='Write every SECONDS seconds. If SECONDS>0 it will produce an infinite loop (default:0.0)')

    json_group = kafka_parser.add_argument_group(title='JSON file options')
    cl_group = kafka_parser.add_argument_group(title='Command-line options')

    json_group.add_argument('-p', '--properties_file', required=False, dest='kafka_props', action='store',
                            help='JSON file with Kafka Producer properties')
    cl_group.add_argument('-b', '--brokers', required=False, dest='kafka_brokers', action='store',
                          help='List of Kafka brokers')

    # SQL commands
    sql_parser = subparsers.add_parser('sql', help='Write to SQL database')
    sql_parser.add_argument('-d', '--driver', required=False, dest='sql_driver', action='store',
                            help='SQL database type ("mysql" or "postgres")')
    sql_parser.add_argument('-sh', '--host', required=True, dest='sql_host', action='store',
                            help='DB Host IP')
    sql_parser.add_argument('-p', '--port', dest='sql_port', type=int, action='store',
                            help='MySQL or PostgreSQL port. Needed only if different than default ones')
    sql_parser.add_argument('-db', '--database', required=True, dest='sql_database', action='store',
                            help='MySQL or PostgreSQL database')
    sql_parser.add_argument('-u', '--username', required=True, dest='sql_username', action='store',
                            help='MySQL or PostgreSQL username')
    sql_parser.add_argument('-pw', '--password', required=True, dest='sql_password', action='store',
                            help='MySQL or PostgreSQL password')
    sql_parser.add_argument('-n', '--number-lines', dest='num_lines', type=int, default=10, action='store',
                            help='Number of lines to generate (default: 10)')
    sql_parser.add_argument('-s', '--sleep-loop', dest='seconds', type=float, default=0.0, action='store',
                            help='Write every SECONDS seconds. If SECONDS>0 it will produce an infinite loop (default:0.0)')

    print(parser.parse_args())
    args = parser.parse_args()
    if args.seconds > 0:
        infinite = True
    else:
        infinite = False

    # Generate LOGS
    if 'log_file_path' in args:

        if args.log_file_name is not None:
            output_file_name = args.log_file_name
        else:
            timestr = time.strftime('%Y%m%d-%H%M%S')
            output_file_name = 'access_log_' + timestr + '.log'

        if not os.path.exists(args.log_file_path):
            os.makedirs(args.log_file_path)

        f = open(args.log_file_path + '/' + output_file_name, 'w')

        from generator.templates.apache_logs_template import ApacheLogsTemplate
        gen = DataGenerator(ApacheLogsTemplate(type="CLF"))

        while True:
            for i in range(args.num_lines):
                f.write(gen.generate())
                f.flush()
            if infinite:
                time.sleep(args.seconds)
            else:
                break

    # Generate data to send to Kafka
    elif 'kafka_topic' in args:
        topic = args.kafka_topic
        properties = args.kafka_props if 'kafka_props' in args else None
        brokers = args.kafka_brokers if 'kafka_brokers' in args else None

        if properties:
            producer = Producer.fromfilename(properties)
        else:
            props = {}
            props.setdefault("client.id", "Fake-Data-Generator")
            props["bootstrap.servers"] = brokers
            props["security.protocol"] = "plaintext"
            producer = Producer.fromdict(props)

        from generator.templates.credit_card_template import CreditCardTemplate
        gen = DataGenerator(CreditCardTemplate(delimiter=","))

        while True:
            for i in range(args.num_lines):
                producer.send(topic=topic, value=gen.generate(), flush=False)
            producer.flush(True)
            if infinite:
                time.sleep(args.seconds)
            else:
                break

    # Generate data to insert into SQL database
    else:
        driver = args.sql_driver
        host = args.sql_host
        database = args.sql_database
        username = args.sql_username
        password = args.sql_password
        port = args.sql_port if 'sql_port' in args else None

        sql_conn = SQLConnector(driver=driver, host=host, port=port, database=database, username=username,
                                password=password)
        sql_conn.create_table()

        from generator.templates.credit_card_template import CreditCardTemplate
        gen = DataGenerator(CreditCardTemplate(format="json"))

        while True:
            for i in range(args.num_lines):
                query = ("INSERT INTO credit_cards_example "
                         "(owner_name, iban, credit_card_number, credit_card_provider) "
                         "VALUES (%(owner_name)s, %(iban)s, %(credit_card_number)s, %(credit_card_provider)s)")
                sql_conn.insert_exec(query=query, values=gen.generate())
            if infinite:
                time.sleep(args.seconds)
            else:
                break


if __name__ == "__main__":
    main()
