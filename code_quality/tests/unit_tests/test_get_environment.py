"""
Unit tests for the "get_environment" function. Designed to be run from the project's top
level.
"""

from jinja2 import Environment

from script.ssm_to_ses import get_environment


def test_returns_expected_object():
    """
    Does get_environment return a jinja2.Environment object?
    """

    response = get_environment()

    assert isinstance(response, Environment)
