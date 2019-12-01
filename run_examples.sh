#!/bin/bash
./v/bin/python syphon.py -c ./example/config-kc.txt
./v/bin/python syphon.py -c ./example/config-bson.txt
./v/bin/python syphon.py -c ./example/config-avro.txt
./v/bin/python syphon.py -c ./example/config-proto.txt
./v/bin/python syphon.py -c ./example/config-capnp.txt --capnp-packed
