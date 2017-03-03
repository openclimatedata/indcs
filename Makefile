all: venv download-indcs

download-indcs: process
	./venv/bin/python scripts/download.py

process:
	./venv/bin/python scripts/process.py

venv: scripts/requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -Ur scripts/requirements.txt
	touch venv

clean:
	rm -rf data/*

.PHONY: clean process download-indcs
