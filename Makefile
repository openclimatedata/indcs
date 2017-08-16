all: process

process: venv
	./venv/bin/python scripts/process.py

venv: scripts/requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install pip --upgrade
	./venv/bin/pip install setuptools --upgrade
	./venv/bin/pip install -Ur scripts/requirements.txt
	touch venv

clean:
	rm -rf data/*
	rm -rf cache/*
	rm -rf pdfs/*

clean-venv:
	rm -rf venv

.PHONY: clean clean-venv process
