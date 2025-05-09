# python-pytest-aws

A Python Pytest framework for AWS services.

## Overview

This project provides the structure for a Python testing framework for a script that interacts with AWS services. As its subject, it also contains a rudimentary script that accepts the names of AWS SSM parameters, collects them from the Parameter Store and then emails a recipient with the parameter values using AWS's Simple Email Service. This script exists primarily to support the testing framework and code quality tools.

## How to use

1. Clone or fork this project.
2. Replace the contents of the `script` directory with your own code.
3. Update the test suite to test your code, using the pre-existing patterns (see the [tools.py file](/code_quality/tests/tools.py) and various conftest.py files).
4. Update your [.pre-commit-config.yaml file](/.pre-commit-config.yaml) with your own Ruff linting configuration.

## Code quality

### Linting

This project uses [Astral-sh's Ruff](https://docs.astral.sh/ruff/) to lint the codeset. To install the tool from the project's root directory, run:

```sh
pip install -r ./code_quality/lint/requirements.txt
```

Ruff configuration is managed in the [pyproject.toml file](/code_quality/pyproject.toml).

To check the code, run:

```sh
ruff check --config "./code_quality/pyproject.toml"
```

Auto-fix some lint errors using the `--fix` flag.

Use Ruff to format your code with:

```sh
ruff format --config "./code_quality/pyproject.toml"
```

### Testing

This project comes with a suite of unit, integration and end-to-end tests. To ensure the flexibility of the codebase, tests utilise random values wherever the program accepts values that are not fixed; wherever the program accepts a list of values, tests supply a random number.

#### Pre-requisites

To run this project's tests, first, from the project's root directory, install the project's dependencies with:

```sh
pip install -r ./script/requirements.txt
```

Then, again from the project's root directory, install its test requirements with:

```sh
pip install -r ./code_quality/tests/requirements/requirements.txt
```

To run end-to-end tests, install those requirements with:

```sh
pip install -r ./code_quality/tests/requirements/end_to_end/requirements.txt
```

#### Unit tests

A suite of unit tests with 100% code coverage is included in this framework. Interactions with AWS services are stubbed out using the [botocore Stubber](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html). A helper method is provided in the [tools.py file](/code_quality/tests/tools.py) to facilitate stubbing.

Unit tests can be run from the project's root directory using:

```sh
coverage run -m pytest -vv code_quality/tests/unit_tests/* --log-cli-level="debug" && coverage report --omit "code_quality/**/*" --rcfile "./code_quality/pyproject.toml" -m
```

### Integration tests

Integration tests are provided to confirm inter-connected functionality where possible. Code coverage is not measured for integration tests. If AWS interactions need to be mocked out, use `mocker.patch`.

Run integration tests from the project's root directory using:

```sh
coverage run -m pytest -vv code_quality/tests/integration_tests/* --log-cli-level="debug"
```

### End-to-end tests

End-to-end tests should test a program's functionality across all use cases. Code coverage should be measured, and full coverage should be the goal. Interactions with AWS services should be mocked using the [moto library](https://docs.getmoto.org/en/latest/docs/getting_started.html). Build AWS infrastructure within Pytest fixtures for your end-to-end tests to interact with.

You can run end-to-end tests from the project's root directory using:

```sh
coverage run -m pytest -vv code_quality/tests/end_to_end_tests/* --log-cli-level="debug" && coverage report --omit "code_quality/**/*" --rcfile "./code_quality/pyproject.toml" -m
```

### Pre-Commit

This project utilises [pre-commit](https://pre-commit.com/) to reduce the risk of badly formatted or otherwise low-quality code being committed. The tool runs a series of lint checks, including Ruff, and also runs the project's test suite to prevent breaking changes from being committed. Pre-commit config is managed in the [.pre-commit-config.yaml file](/.pre-commit-config.yaml).

To install pre-commit, run:

```sh
pip install pre-commit
```

Install all hooks with:

```sh
pre-commit install
```

Then run pre-commit against all files using:

```sh
pre-commit run --all-files
```

Once you have confirmed that pre-commit is working, you should not need to run it manually again; it will run automatically when you commit or push code.

### CI (GitHub Actions)

To further ensure code quality, pushes to branch trigger a [GitHub Actions](https://github.com/features/actions) pipeline that runs Ruff checks and the project's test suite.
