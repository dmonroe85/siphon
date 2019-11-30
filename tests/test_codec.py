import unittest

from lib import codec

message = {
    'a': 3.3,
    'b': 'b',
    'c': None,
    'd': [1, 2, 3],
    'e': {
        'f': 1,
    }
}

kc_schema_file = './tests/test-kc.json'

avro_file = './tests/test.avro'

capnp_file = './tests/test.capnp'
capnp_class = 'Test'
# Because of how capnproto handles nullable fields
capnp_msg = {**message}
capnp_msg['cNull'] = None
del capnp_msg['c']

proto_compile_path = './tests/tests'
proto_message_name = 'Test'

class TestCodec(unittest.TestCase):

    def test_json(self):
        encoded = codec.dict_to_json(message)
        recovered = codec.json_to_dict(encoded)
        self.assertEqual(recovered, message)

    def test_kc_json(self):
        encoded = codec.dict_to_kc_json(kc_schema_file)(message)
        recovered = codec.kc_json_to_dict(encoded)
        self.assertTrue(recovered, message)

    def test_bson(self):
        encoded = codec.dict_to_bson(message)
        recovered = codec.bson_to_dict(encoded)
        self.assertEqual(recovered, message)

    def test_avro(self):
        encoded = codec.dict_to_avro(avro_file)(message)
        recovered = codec.avro_to_dict(avro_file)(encoded)
        self.assertEqual(recovered, message)

    def test_msgpack(self):
        encoded = codec.dict_to_msgpack(message)
        recovered = codec.msgpack_to_dict(encoded)
        self.assertEqual(recovered, message)

    def test_capnproto(self):
        encoded = codec.dict_to_capnp(capnp_file, capnp_class)(capnp_msg)
        recovered = codec.capnp_to_dict(capnp_file, capnp_class)(encoded)
        # Because CapnProto uses more limited precision
        self.assertTrue(abs(recovered['a'] - capnp_msg['a']) < 1e-7)
        del recovered['a']
        del capnp_msg['a']
        self.assertEqual(recovered, capnp_msg)

    def test_protobuf(self):
        encoded = codec.dict_to_proto(proto_compile_path, proto_message_name)(message)
        recovered = codec.proto_to_dict(proto_compile_path, proto_message_name)(encoded)
        # Because of how proto handles optional
        recovered['c'] = None
        self.assertEqual(recovered, message)

