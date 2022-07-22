# reads in .env file any time a target is invoked
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

pip-install:
	pip install -r requirements.txt -r requirements-dev.txt

run-tests:
	pytest -v

run-unit-tests:
	pytest -v python/tests/unit

run-e2e-tests:
	pytest -rx python/tests/e2e