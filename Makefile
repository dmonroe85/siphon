clean:
	rm -rf **/__pycache__

clean-proto:
	rm -rf ./tests/tests

clean-all: clean clean-proto
	rm -rf v/

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
