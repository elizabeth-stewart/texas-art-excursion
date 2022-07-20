# reads in .env file any time a target is invoked
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

run-tests:
	pytest -v