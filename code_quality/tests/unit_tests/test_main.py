"""
Unit tests for the "main" function. Designed to be run from the project's top level.
"""

from script.ssm_to_ses import main


def test_calls_expected_function(
    mocker,
    ssm_to_ses,
    recipient,
    parameter_names,
    caplog,
):
    """
    Does main call functions as expected and log an expected message?
    """

    mock_send_parameters = mocker.patch(f"{ssm_to_ses}.send_parameters")

    main(recipient, parameter_names)

    mock_send_parameters.assert_called_once_with(recipient, parameter_names)
    assert "FUNCTION STARTED" in caplog.text
