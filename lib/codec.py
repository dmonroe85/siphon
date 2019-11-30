import sys
import io
import json

import bson
import avro.schema
import avro.io
import msgpack
import capnp
capnp.remove_import_hook()
from google.protobuf.json_format import MessageToDict, ParseDict

import lib.validate as validate


JSON_CODEC = 'json'
KC_JSON_CODEC = 'kc-json'
BSON_CODEC = 'bson'
AVRO_CODEC = 'avro'
MSGPACK_CODEC = 'msgpack'
CAPNP_CODEC = 'capnproto'
PROTO_CODEC = 'protobuf'

CODECS = [
    JSON_CODEC, KC_JSON_CODEC, BSON_CODEC, AVRO_CODEC, MSGPACK_CODEC,
    CAPNP_CODEC, PROTO_CODEC
]


# JSON
def dict_to_json(d):
	return json.dumps(d).encode('utf-8')

def json_to_dict(j):
	return json.loads(j.decode('utf-8'))


# JSON (Kafka Connect Schema)
def dict_to_kc_json(schema_file):
    with open(schema_file, 'r') as infile:
        kc_schema = json.load(infile)

    def f(d):
        validate.kafka_connect(kc_schema, d)
        return dict_to_json({
            'schema': kc_schema,
            'payload': d
        })

    return f

def kc_json_to_dict(k):
    return json_to_dict(k)['payload']

# BSON
def dict_to_bson(d):
    return bson.dumps(d)

def bson_to_dict(b):
    return bson.loads(b)


# AVRO
def dict_to_avro(schema_file):
    with open(schema_file, 'r') as infile:
        schema = avro.schema.Parse(infile.read())

    def f(d):
        writer = avro.io.DatumWriter(schema)
        byte_stream = io.BytesIO()
        encoder = avro.io.BinaryEncoder(byte_stream)
        writer.write(d, encoder)
        return byte_stream.getvalue()

    return f

def avro_to_dict(schema_file):
    with open(schema_file, 'r') as infile:
        schema = avro.schema.Parse(infile.read())

    def f(a):
        reader = avro.io.DatumReader(schema)
        byte_stream = io.BytesIO(a)
        decoder = avro.io.BinaryDecoder(byte_stream)
        return reader.read(decoder)
    return f


# MSGPACK
def dict_to_msgpack(d):
    return msgpack.packb(d, use_bin_type=True)

def msgpack_to_dict(m):
    return msgpack.unpackb(m, raw=False)


# CAPNPROTO
def dict_to_capnp(schema_file, class_name, packed=False):
    schema = getattr(capnp.load(schema_file), class_name)
    def f(d):
        message = schema.new_message(**d)
        return message.to_bytes_packed() if packed else message.to_bytes()

    return f

def capnp_to_dict(schema_file, class_name, packed=False):
    schema = getattr(capnp.load(schema_file), class_name)
    def f(c):
        message = schema.from_bytes_packed(c) if packed else schema.from_bytes(c)
        return message.to_dict()

    return f


# PROTOBUF
def dict_to_proto(compiled_path, class_name):
    sys.path.append(compiled_path)
    pb2_name = class_name.lower() + '_pb2'
    exec_string = f"from {pb2_name} import {class_name} as PbufMsgWriter"
    exec(exec_string, globals())

    def f(d):
        writer = PbufMsgWriter()
        ParseDict(d, writer)
        return writer.SerializeToString()

    return f

def proto_to_dict(compiled_path, class_name):
    sys.path.append(compiled_path)
    pb2_name = class_name.lower() + '_pb2'
    exec_string = f"from {pb2_name} import {class_name} as PbufMsgReader"
    exec(exec_string, globals())

    def f(p):
        reader = PbufMsgReader()
        reader.ParseFromString(p)
        return MessageToDict(reader)

    return f
