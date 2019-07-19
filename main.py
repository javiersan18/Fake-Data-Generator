import time
import datetime
import argparse
import numpy
import random
from faker import Faker
from kafka.producer import Producer
from tzlocal import get_localzone
local = get_localzone()


def main():
    parser = argparse.ArgumentParser(description='Fake data generator')
    subparsers = parser.add_subparsers(help='Data destination')

    # Logs commands
    list_parser = subparsers.add_parser('log', help='Generate Apache Logs')
    list_parser.add_argument('-o', '--output-path', required=True, dest='log_file_path', action='store', type=str, help='Log path')
    list_parser.add_argument('-n', '--number-lines', dest='log_num_lines', type=int, default=10, action='store', help='Number of lines to generate (default: 10)')
    list_parser.add_argument('-e', '--each-seconds', dest='log_seconds', type=float, default=0.0, action='store', help='If > 0: Write every E seconds.')
    list_parser.add_argument('-f', '--log-format', dest='log_format', help='Log format, Common or Extended Log Format ',
                        choices=['CLF', 'ELF'], default='ELF')

    # Kafka commands
    create_parser = subparsers.add_parser('kafka', help='Write to Apache Kafka')
    create_parser.add_argument('-p', '--properties_file', required=False, dest='kafka_props', action='store', help='JSON file with Kafka Producer properties.')
    create_parser.add_argument('-t', '--topic', required=True,  dest='kafka_topic', action='store', help='Kafka topic')
    create_parser.add_argument('-b', '--brokers', required=False,  dest='kafka_brokers', action='store', help='List of Kafka brokers')
    create_parser.add_argument('-sr', '--schema-registry', required=False,  dest='kafka_schema_registry', action='store', help='URL to Schema-Registry')
    create_parser.add_argument('-n', '--number-lines', dest='log_num_lines', type=int, default=10, action='store',
                             help='Number of lines to generate (default: 10)')
    create_parser.add_argument('-e', '--each-seconds', dest='log_seconds', type=float, default=0.0, action='store',
                             help='If > 0: Write every E seconds.')

    print(parser.parse_args())
    args = parser.parse_args()
    faker = Faker()

    if 'log_file_path' in args:
        timestr = time.strftime('%Y%m%d-%H%M%S')
        otime = datetime.datetime.now()
        output_file_name = 'access_log_' + timestr + '.log'
        f = open(args.log_file_path + '/' + output_file_name,'w')

        http_response = ['200', '404', '500', '301']
        http_verb = ['GET', 'POST', 'DELETE', 'PUT']
        endpoints = ['/clients', '/farms', '/containers', '/routes', '/installations', '/incidences']
        ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

        flag = True
        while flag:

            increment = datetime.timedelta(seconds=args.log_seconds)
            otime += increment

            for i in range(args.log_num_lines):
                otime += datetime.timedelta(microseconds=10)

                ip = faker.ipv4()
                dt = otime.strftime('%d/%b/%Y:%H:%M:%S')
                tz = datetime.datetime.now(local).strftime('%z')
                vrb = numpy.random.choice(http_verb, p=[0.6, 0.1, 0.1, 0.2])

                uri = random.choice(endpoints)

                resp = numpy.random.choice(http_response, p=[0.9, 0.04, 0.02, 0.04])
                byt = int(random.gauss(5000, 50))
                referer = faker.uri()
                useragent = numpy.random.choice(ualist, p=[0.5, 0.3, 0.1, 0.05, 0.05])()

                if args.log_format == 'CLF':
                    f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s\n' % (ip, dt, tz, vrb, uri, resp, byt))
                elif args.log_format == 'ELF':
                    f.write('%s - - [%s %s] "%s %s HTTP/1.0" %s %s "%s" "%s"\n' % (ip, dt, tz, vrb, uri, resp, byt, referer, useragent))
                f.flush()

            if args.log_seconds > 0:
                time.sleep(args.log_seconds)
            else:
                flag = False

    else:
        topic = args.kafka_topic
        properties = args.kafka_props if 'kafka_props' in args else None
        brokers = args.kafka_brokers if 'kafka_brokers' in args else None
        schema_registry = args.kafka_schema_registry if 'kafka_schema_registry' in args else None

        if properties:
            producer = Producer.fromfilename(properties)
        else:
            props = {}
            props.setdefault("client.id", "Fake-Data-Generator")
            props["bootstrap.servers"] = brokers
            props["security.protocol"] = "plaintext"
            props["schema.registry"] = schema_registry
            producer = Producer.fromdict(props)

            from faker.providers import bank
            from faker.providers import credit_card

            faker.add_provider(bank)
            faker.add_provider(credit_card)

        flag = True
        while flag:

            for i in range(args.log_num_lines):
                value = faker.name() + ',' + faker.iban() + ',' + faker.credit_card_number() + ',' + faker.credit_card_provider()
                producer.send(topic=topic, value=value)

            if args.log_seconds > 0:
                time.sleep(args.log_seconds)
            else:
                flag = False


if __name__ == "__main__":
    main()
