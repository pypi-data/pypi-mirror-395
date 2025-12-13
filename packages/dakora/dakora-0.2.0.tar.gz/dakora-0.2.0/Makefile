.PHONY: build clean install test publish help

help:
	@echo "Available commands:"
	@echo "  make build    - Build dakora and dakora-instrumentation packages"
	@echo "  make clean    - Remove build artifacts"
	@echo "  make install  - Install package locally from wheel"
	@echo "  make test     - Run tests"
	@echo "  make publish  - Publish to PyPI"

build: clean
	@echo "Building dakora SDK..."
	uv build --out-dir ../../dist

clean:
	rm -rf dist/ build/ *.egg-info ../../dist/dakora-[0-9]* ../../dist/dakora_[0-9]*
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

install: build
	pip install --force-reinstall ../../dist/dakora-*.whl

test:
	uv run pytest

publish: build
	uv publish
