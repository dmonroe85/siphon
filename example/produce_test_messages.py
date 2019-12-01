from contextlib import closing
import random
import os
import sys

from kafka import KafkaProducer

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import lib.codec as codec

def random_message():
    return {
        'userId': random.randint(0, 1000000),
        'firstName': str(random.randint(0, 1000000)),
        'favoriteSerializer': str(random.randint(0, 1000000)),
    }

def on_error(exception):
    print(exception)
    raise exception


producer_conf = {
    'bootstrap_servers': 'localhost:9092',
    'value_serializer': codec.dict_to_json({}),
}

N_messages = 10000
topic = 'my.test.topic.json'

with closing(KafkaProducer(**producer_conf)) as producer:
    for _ in range(N_messages):
        producer.send(topic, random_message()).add_errback(on_error)
