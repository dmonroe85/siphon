## https://pypi.org/project/ConfigArgParse/

import configargparse

p = configargparse.ArgParser(default_config_files=['~/.kafka_siphon'])
p.add('-c', '--config-file', required=True, is_config_file=True, help='config file path')

parser.add_argument("--source-brokers", help="location of the source kafka servers", type=str)
parser.add_argument("--source-topic", help="source kafka topic", type=str)
parser.add_argument("--sink-brokers", help="location of the sink kafka servers", type=str)
