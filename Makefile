.PHONY: lint
lint:
	@ruff check .

.PHONY: mypy
mypy:
	@mypy finman/

.PHONY: test
test:
	@pytest

.PHONY: all
all: lint mypy test
