# Performs initial setup and runs unit tests
setup: check-deps env pip test



# Checks for system dependencies
check-deps:
	./check_dependencies.sh

# Cleans up python generated files
clean-python:
	rm -rf **/__pycache__

# Cleans up the protobuf files generated for testing
clean-proto:
	rm -rf ./tests/tests
	rm -rf ./example/example

# Cleans up the mounted directories used in docker-compose
clean-data:
	rm -rf ./example/data

# Cleans up the python virtualenv
clean-env:
	rm -rf v/

clean-all: clean-data clean-python clean-proto clean-env



# Builds a new python virtualenv
env: clean-all
	virtualenv -p python3.7 v

# Installs python dependencies with pip
pip:
	v/bin/pip install -r requirements.txt

# Freezes the pip requirements
requirements:
	v/bin/pip freeze > requirements.txt

# Generates the proto definitions for testing
proto: clean-proto
	protoc --python_out=./tests ./tests/test.proto
	protoc --python_out=./example ./example/message.proto

# Runs unit tests
test: clean-python clean-proto proto
	v/bin/python -m unittest discover tests



# Spins up the local kafka broker in docker
docker-up:
	sudo docker-compose -f example/docker-compose.yml up -d

# Brings down the local docker cluster
docker-down:
	sudo docker-compose -f example/docker-compose.yml down

# Publishes data to the local kafka cluster for testing
data:
	v/bin/python example/produce_test_messages.py

# Run example configurations of siphon
run-examples:
	./run_examples.sh

# check the disk size of each kafka topic
analyze-topics:
	tree -sh -P *.log ./example/data/kafka/data/
