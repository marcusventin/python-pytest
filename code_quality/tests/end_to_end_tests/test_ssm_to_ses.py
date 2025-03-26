"""
End to end tests for the ssm_to_ses script. Designed to be run from the project's top
level.
"""

import pytest
from moto.core import DEFAULT_ACCOUNT_ID
from moto.ses import ses_backends

from script.ssm_to_ses import main


@pytest.mark.usefixtures("build_parameters", "build_ses")
def test_sends_expected_email(recipient, parameter_names, set_envs, parameter_values):
    """
    Does ssm_to_ses parameterise and send an expected email?
    """

    main(recipient, parameter_names)
    ses_backend = ses_backends[DEFAULT_ACCOUNT_ID][set_envs["AWS_DEFAULT_REGION"]]
    message = ses_backend.sent_messages[0]

    assert message.source == set_envs["SENDER"]
    assert message.destinations["ToAddresses"] == [recipient]
    assert message.subject == "SSM Parameter Values"
    assert "Your parameter value" in message.body
    for name, value in zip(parameter_names, parameter_values):
        assert f"<li>{name}: {value}</li>" in message.body
