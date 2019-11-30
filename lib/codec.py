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
def dict_to_json(conf):
    def f(d):
        return json.dumps(d).encode('utf-8')

    return f

def json_to_dict(conf):
    def f(j):
        return json.loads(j.decode('utf-8'))

    return f


# JSON (Kafka Connect Schema)
def dict_to_kc_json(conf):
    with open(conf.schema_path, 'r') as infile:
        kc_schema = json.load(infile)

    def f(d):
        validate.kafka_connect(kc_schema, d)
        return dict_to_json(conf)({
            'schema': kc_schema,
            'payload': d
        })

    return f

def kc_json_to_dict(conf):
    def f(k):
        return json_to_dict(conf)(k)['payload']

    return f

# BSON
def dict_to_bson(conf):
    def f(d):
        return bson.dumps(d)

    return f

def bson_to_dict(conf):
    def f(b):
        return bson.loads(b)

    return f


# AVRO
def dict_to_avro(conf):
    with open(conf.schema_path, 'r') as infile:
        schema = avro.schema.Parse(infile.read())

    def f(d):
        writer = avro.io.DatumWriter(schema)
        byte_stream = io.BytesIO()
        encoder = avro.io.BinaryEncoder(byte_stream)
        writer.write(d, encoder)
        return byte_stream.getvalue()

    return f

def avro_to_dict(conf):
    with open(conf.schema_path, 'r') as infile:
        schema = avro.schema.Parse(infile.read())

    def f(a):
        reader = avro.io.DatumReader(schema)
        byte_stream = io.BytesIO(a)
        decoder = avro.io.BinaryDecoder(byte_stream)
        return reader.read(decoder)
    return f


# MSGPACK
def dict_to_msgpack(conf):
    def f(d):
        return msgpack.packb(d, use_bin_type=conf.msgpack_bin_type)

    return f

def msgpack_to_dict(conf):
    def f(m):
        return msgpack.unpackb(m, raw=False)

    return f


# CAPNPROTO
def dict_to_capnp(conf):
    schema = getattr(capnp.load(conf.schema_path), conf.class_name)
    def f(d):
        message = schema.new_message(**d)
        return message.to_bytes_packed() if conf.capnp_packed else message.to_bytes()

    return f

def capnp_to_dict(conf):
    schema = getattr(capnp.load(conf.schema_path), conf.class_name)
    def f(c):
        message = schema.from_bytes_packed(c) if conf.capnp_packed else schema.from_bytes(c)
        return message.to_dict()

    return f


# PROTOBUF
def dict_to_proto(conf):
    sys.path.append(conf.schema_path)
    pb2_name = conf.class_name.lower() + '_pb2'
    exec_string = f"from {pb2_name} import {conf.class_name} as PbufMsgWriter"
    exec(exec_string, globals())

    def f(d):
        writer = PbufMsgWriter()
        ParseDict(d, writer)
        return writer.SerializeToString()

    return f

def proto_to_dict(conf):
    sys.path.append(conf.schema_path)
    pb2_name = conf.class_name.lower() + '_pb2'
    exec_string = f"from {pb2_name} import {conf.class_name} as PbufMsgReader"
    exec(exec_string, globals())

    def f(p):
        reader = PbufMsgReader()
        reader.ParseFromString(p)
        return MessageToDict(reader)

    return f


# Accessors
ENCODERS = {
    JSON_CODEC: dict_to_json,
    KC_JSON_CODEC: dict_to_kc_json,
    BSON_CODEC: dict_to_bson,
    AVRO_CODEC: dict_to_avro,
    MSGPACK_CODEC: dict_to_msgpack,
    CAPNP_CODEC: dict_to_capnp,
    PROTO_CODEC: dict_to_proto,
}

DECODERS = {
    JSON_CODEC: json_to_dict,
    KC_JSON_CODEC: kc_json_to_dict,
    BSON_CODEC: bson_to_dict,
    AVRO_CODEC: avro_to_dict,
    MSGPACK_CODEC: msgpack_to_dict,
    CAPNP_CODEC: capnp_to_dict,
    PROTO_CODEC: proto_to_dict,
}
