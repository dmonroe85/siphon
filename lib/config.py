## https://pypi.org/project/ConfigArgParse/

import sys

import configargparse

from lib.codec import CODECS

parser = configargparse.ArgParser(default_config_files=['~/.kafka_siphon'])
parser.add('-c',
           '--config-file',
           required=True,
           is_config_file=True,
           help='config file path')

# Source Kafka
parser.add_argument("--source-brokers",
                    required=True,
                    help="location of the source kafka servers")
parser.add_argument("--source-topic",
                    required=True,
                    help="source kafka topic")
parser.add_argument("--source-encoding",
                    required=True,
                    choices=CODECS,
                    help="source topic encoding")

# Sink Kafka
parser.add_argument("--sink-brokers",
                    required=True,
                    help="location of the sink kafka servers")
parser.add_argument("--sink-topic",
                    required=True,
                    help="sink kafka topic")
parser.add_argument("--sink-encoding",
                    required=True,
                    choices=CODECS,
                    help="sink topic encoding")


parser.add_argument("--key-fields",
                    help="fields that will be used to generate a new kafka key")

# Codecs
parser.add_argument("--schema-path", help="schema definition or compiled location")
parser.add_argument("--class-name", help="codec class name")
parser.add_argument("--capnp-packed",
                    help="enabled packed capnproto message",
                    action='store_true')
parser.add_argument("--msgpack-bin-type",
                    help="use msgpack bin type",
                    action='store_true')
