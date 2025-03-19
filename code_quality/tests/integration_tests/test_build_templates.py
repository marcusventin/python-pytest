"""
Integration tests for the functionality to parameterise email template files. Designed
to be run from the project's top level.
"""

from script.ssm_to_ses import build_templates


def test_returns_expected_response(mocker, ssm_to_ses, environment, parameters):
    """
    Does build_templates return an expected response?
    """

    mock_get_environment = mocker.patch(
        f"{ssm_to_ses}.get_environment", return_value=environment
    )

    response = build_templates("ssm_to_ses", parameters)

    mock_get_environment.assert_called_once_with()
    for parameter in parameters:
        assert f"{parameter['name']}: {parameter['value']}" in response["html"]
        assert f"{parameter['name']}: {parameter['value']}" in response["txt"]
