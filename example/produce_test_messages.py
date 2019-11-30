from contextlib import closing
import random
import os
import sys

from kafka import KafkaProducer

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from lib.codec import dict_to_json

def random_message():
    return {
        'user_id': random.randint(0, 1000000),
        'first_name': str(random.randint(0, 1000000)),
        'favorite_serializer': str(random.randint(0, 1000000)),
    }

producer_conf = {
    'bootstrap_servers': 'localhost:9092',
    'value_serializer': dict_to_json({}),
}

N_messages = 1000
topic = 'my.test.topic.json'

with closing(KafkaProducer(**producer_conf)) as producer:
    for _ in range(N_messages):
        producer.send(topic, random_message())
