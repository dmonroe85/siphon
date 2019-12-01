from contextlib import closing

from kafka import KafkaConsumer, KafkaProducer

from lib.config import parser
from lib.codec import DECODERS, ENCODERS

conf, _ = parser.parse_known_args()

consumer_conf = {
    'bootstrap_servers': conf.source_brokers,
    'auto_offset_reset': conf.source_auto_offset_reset,
    'consumer_timeout_ms': conf.source_consumer_timeout_ms,
    'value_deserializer': DECODERS[conf.source_encoding](conf),
    'enable_auto_commit': conf.source_enable_auto_commit,
}

producer_conf = {
    'bootstrap_servers': conf.sink_brokers,
    'value_serializer': ENCODERS[conf.sink_encoding](conf),
    'compression_type': conf.sink_compression,
}

with closing(KafkaConsumer(**consumer_conf)) as consumer,\
     closing(KafkaProducer(**producer_conf)) as producer:
    consumer.subscribe([conf.source_topic])
    for message in consumer:
        producer.send(conf.sink_topic, value=message.value)
