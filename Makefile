.PHONY: lint
lint:
	isort src
	black src
	mypy src
	flake8 src

.PHONY: test
test:
	pytest --cov=src --cov-report=term-missing src/tests.py
