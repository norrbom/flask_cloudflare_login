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
	pip install --upgrade pip build && \
	python -m build

install:
	python3 -m venv ./venv
	. ./venv/bin/activate && \
	pip install --upgrade --force-reinstall --find-links ./dist flask_cloudflare_login

publish-test:
	python3 -m venv ./venv
	. ./venv/bin/activate && \
	pip install --upgrade pip twine && \
	twine upload --repository testpypi dist/*

publish:
	python3 -m venv ./venv
	. ./venv/bin/activate && \
	pip install --upgrade pip twine && \
	twine upload --repository pypi dist/*

run:
	python3 -m venv ./venv
	. ./venv/bin/activate && \
	pip install -r ./examples/dash/requirements.txt && \
	export export SECRET_KEY=$(SECRET_KEY) && \
	cd examples/dash && python app.py
