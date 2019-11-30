"""
{
  "schema": {
    "type": "struct",
    "fields": [
      {
        "type": "int64",
        "optional": false,
        "field": "registertime"
      },
      {
        "type": "string",
        "optional": false,
        "field": "userid"
      },
      {
        "type": "string",
        "optional": false,
        "field": "regionid"
      },
      {
        "type": "string",
        "optional": false,
        "field": "gender"
      }
    ],
    "optional": false,
    "name": "ksql.users"
  },
  "payload": {
    "registertime": 1493819497170,
    "userid": "User_1",
    "regionid": "Region_5",
    "gender": "MALE"
  }
}

https://www.confluent.io/blog/kafka-connect-deep-dive-converters-serialization-explained/#json-schemas

https://docs.confluent.io/current/connect/kafka-connect-jdbc/sink-connector/index.html
"""
KC_BOOL_TYPES = []
KC_INT_TYPES = []
KC_LONG_TYPES = []
KC_FLOAT_TYPES = []
KC_STRING_TYPES = []
def kafka_connect(schema, d):
    """ Work In Progress - I want to add type and null checking eventually """
    for field_def in schema['fields']:
        field_name = field_def['field']
        present = field_name in d
        optional = field_def['optional'] if 'optional' in field_def else False
        field_type = field_def['type']

        if not optional and not present:
            error_message = "Could not find required field"
            raise KeyError(error_message)

        value = d[field_name]
        value_type = type(value)
