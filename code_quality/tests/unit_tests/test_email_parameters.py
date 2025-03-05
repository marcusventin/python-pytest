"""
Unit tests for the "email_parameters" function. Designed to be run from the project's
top level.
"""

from script.ssm_to_ses import email_parameters


def test_calls_expected_functions(mocker, ssm_to_ses, templates, recipient, parameters):
    """
    Does email_parameters call expected functions with expected arguments?
    """

    mock_build_templates = mocker.patch(
        f"{ssm_to_ses}.build_templates", return_value=templates
    )
    mock_send_email = mocker.patch(f"{ssm_to_ses}.send_email")

    email_parameters(recipient, parameters)

    mock_build_templates.assert_called_once_with("ssm_to_ses", parameters)
    mock_send_email.assert_called_once_with(recipient, templates)
