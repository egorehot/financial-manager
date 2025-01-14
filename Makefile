.PHONY: lint
lint:
	@ruff check .

.PHONY: mypy
mypy:
	@mypy finman/
