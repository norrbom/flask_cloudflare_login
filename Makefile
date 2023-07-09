SHELL := /bin/bash

.PHONY: test build run

SECRET_KEY         ?=$$(openssl rand -base64 32)

clean:
	rm -fr ./venv

test:
	python3 -m venv ./venv
	. ./venv/bin/activate && \
	export PYTHONPATH=./src && \
	pip install --upgrade pip hatch && \
	hatch run test:black src && \
	hatch run test:isort src && \
	hatch run test:pytest -v

build:
	rm -fr ./dist
	python3 -m venv ./venv
	. ./venv/bin/activate && \
	pip install --upgrade pip hatch && \
	hatch version b && \
	hatch build -t wheel

run:
	. ./venv/bin/activate && \
	pip install -r ./examples/dash/requirements.txt && \
	pip install --upgrade --no-deps --force-reinstall --no-index --find-links ./dist flask_cloudflare && \
	export export SECRET_KEY=$(SECRET_KEY) && \
	cd examples/dash && python app.py
