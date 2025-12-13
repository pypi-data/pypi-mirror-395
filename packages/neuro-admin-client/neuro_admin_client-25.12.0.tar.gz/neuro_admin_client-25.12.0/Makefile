SHELL := /bin/bash

ISORT_TARGETS := neuro_admin_client tests
BLACK_TARGETS := $(ISORT_TARGETS)
MYPY_TARGETS :=  $(ISORT_TARGETS)
FLAKE8_TARGETS:= $(ISORT_TARGETS)

.PHONY: all
all: lint test

.PHONY: setup
setup:
	uv sync --dev
	uv run pre-commit install

.PHONY: format
format: setup
ifdef CI_LINT_RUN
	uv run pre-commit run --all-files --show-diff-on-failure
else
	uv run pre-commit run --all-files
endif


.PHONY: lint
lint: format
	uv run mypy $(MYPY_TARGETS)

.PHONY: test
test:
	uv run pytest --cov=neuro_admin_client --cov-report xml:.coverage.xml tests

.PHONY: clean
clean:
	git clean -fd
