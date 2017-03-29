# Super Oxigen House-Rules - Makefile

# Easy running and setup of the blog server.

.phony: debug, run

export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

run:
	python3 hrules.py

debug:
	python3 hrules.py --debug
