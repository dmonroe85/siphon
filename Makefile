clean-python:
	rm -rf **/__pycache__

clean-proto:
	rm -rf ./tests/tests

clean-data:
	rm -rf ./example/data

clean-env:
	rm -rf v/

clean-all: clean-data clean-python clean-proto clean-env


env: clean-all
	virtualenv -p python3.7 v

pip:
	v/bin/pip install -r requirements.txt

proto: clean-proto
	protoc --python_out=./tests ./tests/test.proto

test: clean proto
	v/bin/python -m unittest discover tests

requirements:
	pip freeze > requirements.txt

setup: env pip test


docker-up:
	sudo docker-compose -f example/docker-compose.yml up -d

docker-down:
	sudo docker-compose -f example/docker-compose.yml down

