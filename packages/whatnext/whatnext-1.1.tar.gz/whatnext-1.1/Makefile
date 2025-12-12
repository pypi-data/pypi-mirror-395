ifndef CI
ifndef VIRTUAL_ENV
$(error Development has to happen inside venv, whatnext is also installed globally.)
endif
endif

.PHONY: test flake8 pytest bats

test: flake8 pytest bats

flake8:
	flake8 whatnext tests

pytest: flake8
	pytest tests/

bats:
	bats tests/*.bats
