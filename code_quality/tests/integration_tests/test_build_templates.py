"""
Integration tests for the functionality to parameterise email template files. Designed
to be run from the project's top level.
"""

from script.ssm_to_ses import build_templates


def test_returns_expected_response(parameters):
    """
    Does build_templates return an expected response?
    """

    response = build_templates("ssm_to_ses", parameters)

    for parameter in parameters:
        assert f"{parameter["name"]}: {parameter["value"]}" in response["txt"]
        assert f"<li>{parameter["name"]}: {parameter["value"]}</li>" in response["html"]
