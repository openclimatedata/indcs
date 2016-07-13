all: download-indcs

download-indcs: process
	python scripts/download.py

process:
	python scripts/process.py

clean:
	rm -rf data/*

.PHONY: clean process download-indcs
