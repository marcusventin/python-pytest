"""
Unit tests for the "send_email" function. Designed to be run from the project's top
level.
"""

from code_quality.tests.tools import random_string, stub_boto_client
from script.ssm_to_ses import send_email


def test_makes_expected_call(set_envs, recipient, templates):
    """
    Does send_email make an expected call and return an expected response?
    """

    send_email_response = {"MessageId": random_string(12)}
    expected_parameters = {
        "Source": set_envs["SENDER"],
        "Destination": {"ToAddresses": [recipient]},
        "Message": {
            "Subject": {
                "Data": "SSM Parameter Values",
                "Charset": "utf-8"
            },
            "Body": {
                "Text": {"Data": templates["txt"], "Charset": "utf-8"},
                "Html": {"Data": templates["html"], "Charset": "utf-8"},
            },
        },
    }
    client = stub_boto_client(
        "ses", "send_email", send_email_response, expected_parameters
    )

    response = send_email(recipient, templates, client=client)

    assert response == send_email_response
