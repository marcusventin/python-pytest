"""
Fixtures to facilitate the testing of the ssm_to_ses script.
"""

import os
from random import randint

import pytest
from jinja2 import Environment, FileSystemLoader

from code_quality.tests.tools import random_string


@pytest.fixture(name="ssm_to_ses")
def fixture_ssm_to_ses_path() -> str:
    """
    Path to the ssm_to_ses script from the project's top level.
    """

    return "script.ssm_to_ses"


@pytest.fixture(name="set_envs", autouse=True)
def fixture_set_environment_variables(monkeypatch) -> dict[str]:
    """
    Define a set of env variables for testing purposes, monkeypatch them, and return a
    dictionary containing their values.
    """

    env_vars = {
        "AWS_ACCESS_KEY_ID": random_string(16),
        "AWS_SECRET_ACCESS_KEY": random_string(16),
        "AWS_DEFAULT_REGION": "eu-west-2",
        "SENDER": random_string(8),
    }
    monkeypatch.setattr(os, "environ", env_vars)
    return env_vars


@pytest.fixture(name="recipient")
def fixture_recipient() -> str:
    """
    Return a string representing a mock email address for a recipient.
    """

    return random_string(10)


@pytest.fixture(name="parameters")
def fixture_parameters() -> list[dict[str]]:
    """
    Return a list of dictionaries representing mock SSM parameter details.
    """

    return [
        {"name": random_string(6), "value": random_string(8)}
        for i in range(randint(1, 10))
    ]


@pytest.fixture(name="parameter_names")
def fixture_parameter_names(parameters: list[dict[str]]) -> list[str]:
    """
    Return a list of strings representing mock SSM parameter names.

    Parameters
    ----------
    parameters: list[dict[str]]
        A list of dictionaries containing "name" and "value" values representing mock
        parameter data.
    """

    return [parameter["name"] for parameter in parameters]


@pytest.fixture(name="parameter_values")
def fixture_parameter_values(parameters: list[dict[str]]) -> str:
    """
    Return a list of strings representing mock SSM parameter values.

    Parameters
    ----------
    parameters: list[dict[str]]
        A list of dictionaries containing "name" and "value" values representing mock
        parameter data.
    """

    return [parameter["value"] for parameter in parameters]


@pytest.fixture(name="environment")
def fixture_jinja2_environment() -> Environment:
    """
    Return a Jinja2 Environment pointed at a templates directory.
    """

    return Environment(loader=FileSystemLoader("script/templates/"), autoescape=True)


@pytest.fixture(name="templates")
def fixture_email_templates() -> dict[str]:
    """
    Return a dictionary containing mock rendered email templates.
    """

    return {"txt": random_string(8), "html": random_string(8)}
