# Siphon

A tool intended to:
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
* `make docker-up` to run kafka and zookeeper locally; wait until they are healthy
    * use `docker ps` to check the health of both services.
* `make data` to publish json data to kafka
* `make run-examples` to iterate through the supported serializer configurations
* `make analyze-topics` to check the disk size of each kafka topic


## Serializer Comparison Example

This test was done generating 10000 json test messages and using siphon to move
and convert to each different serializer.

```bash
tree -sh -P *.log ./example/data/kafka/data/
./example/data/kafka/data/
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
    └── [272K]  00000000000000000000.log

8 directories, 8 files

```
