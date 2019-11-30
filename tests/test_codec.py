import unittest

from lib import codec
from lib.config import parser

message = {
    'a': 3.3,
    'b': 'b',
    'c': None,
    'd': [1, 2, 3],
    'e': {
        'f': 1,
    }
}

# File Paths
config_file = './tests/config.txt'
kc_schema_file = './tests/test-kc.json'
avro_file = './tests/test.avro'
capnp_file = './tests/test.capnp'
capnp_class = 'Test'
proto_compile_path = './tests/tests'
proto_message_name = 'Test'

base_args = ['-c', config_file]

class TestCodec(unittest.TestCase):

    def test_json(self):
        conf, _ = parser.parse_known_args(base_args)
        encoded = codec.dict_to_json(conf)(message)
        recovered = codec.json_to_dict(conf)(encoded)
        self.assertEqual(recovered, message)

    def test_kc_json(self):
        conf, _ = parser.parse_known_args(base_args + ['--schema-path', kc_schema_file])
        encoded = codec.dict_to_kc_json(conf)(message)
        recovered = codec.kc_json_to_dict(conf)(encoded)
        self.assertTrue(recovered, message)

    def test_bson(self):
        conf, _ = parser.parse_known_args(base_args)
        encoded = codec.dict_to_bson(conf)(message)
        recovered = codec.bson_to_dict(conf)(encoded)
        self.assertEqual(recovered, message)

    def test_avro(self):
        conf, _ = parser.parse_known_args(base_args + ['--schema-path', avro_file])
        encoded = codec.dict_to_avro(conf)(message)
        recovered = codec.avro_to_dict(conf)(encoded)
        self.assertEqual(recovered, message)

    def test_msgpack(self):
        conf, _ = parser.parse_known_args(base_args + ['--msgpack-bin-type'])
        encoded = codec.dict_to_msgpack(conf)(message)
        recovered = codec.msgpack_to_dict(conf)(encoded)
        self.assertEqual(recovered, message)

    def test_capnproto(self):
        conf, _ = parser.parse_known_args(base_args + [
            '--schema-path', capnp_file,
            '--class-name', capnp_class,
            '--capnp-packed',
        ])

        # Because of how capnproto handles nullable fields
        capnp_msg = {**message}
        capnp_msg['cNull'] = None
        del capnp_msg['c']

        encoded = codec.dict_to_capnp(conf)(capnp_msg)
        recovered = codec.capnp_to_dict(conf)(encoded)

        # Because CapnProto uses more limited precision
        self.assertTrue(abs(recovered['a'] - capnp_msg['a']) < 1e-7)
        del recovered['a']
        del capnp_msg['a']
        self.assertEqual(recovered, capnp_msg)

    def test_protobuf(self):
        conf, _ = parser.parse_known_args(base_args + [
            '--schema-path', proto_compile_path,
            '--class-name', proto_message_name,
        ])

        encoded = codec.dict_to_proto(conf)(message)
        recovered = codec.proto_to_dict(conf)(encoded)
        # Because of how protobuf handles optional
        recovered['c'] = None
        self.assertEqual(recovered, message)

