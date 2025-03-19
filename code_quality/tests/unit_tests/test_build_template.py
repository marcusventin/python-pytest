"""
Unit tests for the "build_template" function. Designed to be run from the project's top
level.
"""

from script.ssm_to_ses import build_template


def test_returns_expected_response(environment, parameters):
    """
    Does build_template return an expected response?
    """

    response = build_template(environment, "ssm_to_ses.txt", parameters)

    assert "Your parameter value" in response
    for parameter in parameters:
        assert f"{parameter['name']}: {parameter['value']}" in response
