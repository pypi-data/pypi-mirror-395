.PHONY: setup-dev flake8 isort isort-fix mypy lint build clean

NAME = ytrssil

FILES_PY = $(shell find $(CURDIR)/$(NAME) -type f -name "*.py")

setup-dev:
	uv sync

flake8:
	@uv run flake8 $(FILES_PY)

isort:
	@uv run isort -c $(FILES_PY)

isort-fix:
	@uv run isort $(FILES_PY)

mypy:
	@uv run mypy --strict $(FILES_PY)

lint: flake8 isort mypy

build:
	uv build

clean:
	rm -rf $(CURDIR)/build
	rm -rf $(CURDIR)/dist
	rm -rf $(CURDIR)/$(NAME).egg-info

publish:
	@git checkout $(shell git tag | sort -V | tail -n1) >/dev/null 2>&1
	@$(MAKE) clean > /dev/null
	@$(MAKE) build > /dev/null
	@uv publish
	@$(MAKE) clean > /dev/null
	@git switch main >/dev/null 2>&1
