# auris-tools

[![PyPI version](https://img.shields.io/pypi/v/auris-tools.svg)](https://pypi.org/project/auris-tools/)
[![Documentation Status](https://readthedocs.org/projects/auris-tools/badge/?version=latest)](https://auris-tools.readthedocs.io/en/latest/?badge=latest)
[![CI for Develop Branch](https://github.com/AurisAASI/auris-tools/actions/workflows/ci_develop.yml/badge.svg?branch=develop)](https://github.com/AurisAASI/auris-tools/actions/workflows/ci_develop.yml)
[![CI for Develop Branch](https://github.com/AurisAASI/auris-tools/actions/workflows/ci_develop.yml/badge.svg?branch=main)](https://github.com/AurisAASI/auris-tools/actions/workflows/ci_develop.yml)
[![codecov](https://codecov.io/gh/AurisAASI/auris-tools/graph/badge.svg?token=08891W8HP2)](https://codecov.io/gh/AurisAASI/auris-tools)

The swiss knife tools to coordinates cloud frameworks with an easy for Auris platforms

## Installation

This project requires **Python 3.10** and uses [Poetry](https://python-poetry.org/) for dependency management.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AurisAASI/auris-tools.git
   cd auris-tools
   ```
2. **Install Poetry (if not already installed):**
   ```bash
   pip install poetry
   ```
3. **Install dependencies:**
   ```bash
   poetry install
   ```

---

## Project Structure

The main classes and modules are organized as follows:

```
/auris_tools
├── __init__.py
├── configuration.py         # AWS configuration utilities
├── databaseHandlers.py      # DynamoDB handler class
├── officeWordHandler.py     # Office Word document handler
├── storageHandler.py        # AWS S3 storage handler
├── textractHandler.py       # AWS Textract handler
├── utils.py                 # Utility functions
├── geminiHandler.py         # Google Gemini AI handler
```

---

## Testing & Linting

- **Run all tests:**
  ```bash
  task test
  ```
- **Run linter (blue and isort):**
  ```bash
  task lint
  ```

Test coverage and linting are enforced in CI. Make sure all tests pass and code is linted before submitting a PR.

## Documentation

We use MkDocs with Material theme for our documentation:

- **Run documentation server locally:**
  ```bash
  task docs
  ```
- **Build documentation:**
  ```bash
  task docs-build
  ```

The documentation is automatically published to Read the Docs when changes are pushed to the main branch.

---
