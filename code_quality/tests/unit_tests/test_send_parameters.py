"""
Unit tests for the "send_parameters" function. Designed to be run from the project's top
level.
"""

from script.ssm_to_ses import send_parameters


def test_calls_expected_functions(
    mocker,
    ssm_to_ses,
    parameters,
    recipient,
    parameter_names,
):
    """
    Does send_parameters call expected functions with expected arguments?
    """

    mock_get_parameter_values = mocker.patch(
        f"{ssm_to_ses}.get_parameter_values",
        return_value=parameters,
    )
    mock_email_parameters = mocker.patch(f"{ssm_to_ses}.email_parameters")

    send_parameters(recipient, parameter_names)

    mock_get_parameter_values.assert_called_once_with(parameter_names)
    mock_email_parameters.assert_called_once_with(recipient, parameters)
