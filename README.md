# Siphon

A library to:
* move data from one kafka topic to another
* within or across clusters
* with the ability to change serialization format
* with the ability to change the kafka partition key (eventually)

## Getting Started

A lot of helpful utilities are scripted as `make` commands.  Check the root
`Makefile`for reference.

To perform initial setup and run unit tests, run `make setup`.

To run siphon, run `v/bin/python siphon.py <options>`

For help with configuration, run `v/bin/python siphon.py --help`.

To get started with a local kafka environment:
* `make docker-up` to run kafka and zookeeper locally
* `make data` to publish json data to kafka


## Serializer Comparison

This test was done generating data from

```bash
$ tree -sh -P *.log
.
├── [4.0K]  __confluent.support.metrics-0
│   └── [   0]  00000000000000000000.log
├── [4.0K]  my.test.topic.avro-0
│   └── [252K]  00000000000000000000.log
├── [4.0K]  my.test.topic.bson-0
│   └── [779K]  00000000000000000000.log
├── [4.0K]  my.test.topic.capnp-0
│   └── [359K]  00000000000000000000.log
├── [4.0K]  my.test.topic.json-0
│   └── [808K]  00000000000000000000.log
├── [4.0K]  my.test.topic.kc-0
│   └── [3.5M]  00000000000000000000.log
├── [4.0K]  my.test.topic.msgpack-0
│   └── [622K]  00000000000000000000.log
└── [4.0K]  my.test.topic.protobuf-0
    └── [271K]  00000000000000000000.log

8 directories, 8 files
```
