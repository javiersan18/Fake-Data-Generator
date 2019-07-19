import time
import argparse
from kafka.producer import Producer
from generator.data_generator import DataGenerator


def main():
    parser = argparse.ArgumentParser(description='Fake data generator')
    subparsers = parser.add_subparsers(help='Data destination')

    # Logs commands
    log_parser = subparsers.add_parser('log', help='Generate Apache Logs')
    log_parser.add_argument('-o', '--output-path', required=True, dest='log_file_path', action='store', type=str,
                            help='Log path')
    log_parser.add_argument('-n', '--number-lines', dest='num_lines', type=int, default=10, action='store',
                            help='Number of lines to generate (default: 10)')
    log_parser.add_argument('-s', '--sleep-loop', dest='seconds', type=float, default=0.0, action='store',
                            help='Write every SECONDS seconds. If SECONDS>0 infinite loop (default:0.0)')
    log_parser.add_argument('-f', '--log-format', dest='log_format', help='Log format, Common or Extended Log Format ',
                            choices=['CLF', 'ELF'], default='ELF')

    # Kafka commands
    kafka_parser = subparsers.add_parser('kafka', help='Write to Apache Kafka')
    kafka_parser.add_argument('-t', '--topic', required=True, dest='kafka_topic', action='store', help='Kafka topic')
    kafka_parser.add_argument('-n', '--number-lines', dest='num_lines', type=int, default=10, action='store',
                              help='Number of lines to generate (default: 10)')
    kafka_parser.add_argument('-s', '--sleep-loop', dest='seconds', type=float, default=0.0, action='store',
                              help='Write every SECONDS seconds. If SECONDS>0 infinite loop (default:0.0)')

    json_group = kafka_parser.add_argument_group(title='JSON file options')
    cl_group = kafka_parser.add_argument_group(title='Command-line options')

    json_group.add_argument('-p', '--properties_file', required=False, dest='kafka_props', action='store',
                            help='JSON file with Kafka Producer properties.')
    cl_group.add_argument('-b', '--brokers', required=False, dest='kafka_brokers', action='store',
                          help='List of Kafka brokers')

    print(parser.parse_args())
    args = parser.parse_args()
    if args.seconds > 0:
        infinite = True
    else:
        infinite = False

    # Generate LOGS
    if 'log_file_path' in args:

        timestr = time.strftime('%Y%m%d-%H%M%S')
        output_file_name = 'access_log_' + timestr + '.log'
        f = open(args.log_file_path + '/' + output_file_name, 'w')

        from generator.templates.apache_logs_template import ApacheLogsTemplate
        gen = DataGenerator(ApacheLogsTemplate(type="CLF"))

        while infinite:
            for i in range(args.num_lines):
                f.write(gen.generate())
                f.flush()
            if infinite:
                time.sleep(args.log_seconds)

    # Generate data to send to Kafka
    else:
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

        while infinite:
            for i in range(args.num_lines):
                producer.send(topic=topic, value=gen.generate(), flush=False)
            producer.flush(True)
            if infinite:
                time.sleep(args.seconds)


if __name__ == "__main__":
    main()
