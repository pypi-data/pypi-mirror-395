.PHONY: all clean build install test publish uninstall dist-clean

PACKAGE_NAME := ray-cli
DIST_DIR := dist
TEST_DIR := .pytest_cache .pytype .tox
WHEEL := $(DIST_DIR)/*.whl

all: install

build: dist-clean
	@echo "Building package..."
	uv build

install: build
	@echo "Installing $(PACKAGE_NAME) via uv..."
	uv tool install --force $(WHEEL)

test:
	@echo "Running tests with tox..."
	tox

publish: test build
	@echo "Publishing $(PACKAGE_NAME) to PyPI..."
	uv publish --token "$$(security find-generic-password -w -s pypi-token)"

clean: dist-clean test-clean uninstall

uninstall:
	@echo "Uninstalling $(PACKAGE_NAME) via uv..."
	uv tool uninstall $(PACKAGE_NAME)

dist-clean:
	@echo "Cleaning distribution files..."
	rm -rf $(DIST_DIR)

test-clean:
	@echo "Cleaning test files..."
	rm -rf $(TEST_DIR)
