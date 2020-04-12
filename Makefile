.PHONY: init
init:
	pipenv install

.PHONY: test
test:
	make lint unit_test

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

.PHONY: run_single
run_single:
	pipenv run python main.py single

.PHONY: run_eval
run_eval:
	pipenv run python main.py eval
	
.PHONY: run_ex
run_ex:
	pipenv run python main.py example