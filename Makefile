.PHONY: init
init:
	pipenv install

.PHONY: run
run:
	pipenv run python main.py

.PHONY: unit_test
unit_test:
	pipenv run pytest tests/unit_tests 

.PHONY: lint
lint:
	make pylint flake8 black_lint sort_import_check static_check

.PHONY: format
format:
	pipenv run black .

.PHONY: flake8
flake8:
	pipenv run flake8

.PHONY: pylint
pylint:
	pipenv run pylint --rcfile=setup.cfg src/

.PHONY: black_lint
black_lint:
	pipenv run black --check --diff .

.PHONY: static_check
static_check:
	pipenv run mypy .

.PHONY: sort_import
sort_import:
	pipenv run isort -rc .

.PHONY: sort_import_check
sort_import_check:
	pipenv run isort -rc . -c
