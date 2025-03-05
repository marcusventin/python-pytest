"""
Unit tests for the "get_parameter_value" function. Designed to be run from the project's
top level.
"""

from random import randint

from code_quality.tests.tools import random_string, stub_boto_client
from script.ssm_to_ses import get_parameter_values


def test_returns_expected_value(parameters, parameter_names, caplog):
    """
    Does get_parameter_values return an expected value and log an expected message?
    """

    get_parameters_response = {
        "Parameters": [
            {
                "Name": parameter["name"],
                "Type": "SecureString",
                "Value": parameter["value"],
                "Version": randint(1, 100),
                "ARN": random_string(12),
                "DataType": "text",
            }
            for parameter in parameters
        ]
    }
    expected_parameters = {
        "Names": parameter_names,
        "WithDecryption": True,
    }
    client = stub_boto_client(
        "ssm", "get_parameters", get_parameters_response, expected_parameters
    )

    response = get_parameter_values(parameter_names, client=client)

    assert response == parameters
    assert f"Getting values of parameters {parameter_names}" in caplog.text
