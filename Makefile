PYTHON := python3
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: setup env venv install

setup: env venv install check-version
	@echo "\n\n\t\tNow fill in your .env file"

env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
	fi

venv:
	$(PYTHON) -m venv $(VENV)

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

check-version:
	@EXPECTED=$$(cat .python-version); \
	CURRENT=$$(python3 --version | cut -d' ' -f2); \
	[ "$$EXPECTED" = "$$CURRENT" ] || echo "Warning: expected $$EXPECTED, got $$CURRENT"

up:
	$(PYTHON) src/front/auth_window/auth_window.py