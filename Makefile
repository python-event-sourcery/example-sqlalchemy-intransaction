SRCS ?= ${wildcard *.py}

.PHONY: lint
lint:
	isort $(SRCS)
	black $(SRCS)
	mypy $(SRCS)
	flake8 $(SRCS)

.PHONY: test
test:
	pytest $(addprefix --cov ,$(SRC)) tests.py
