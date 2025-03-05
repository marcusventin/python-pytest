"""
A set of functions to faciltiate automated tests.
"""

import random
import string

import boto3
from botocore.stub import Stubber


def random_string(string_length: int) -> str:
    """
    Generate a random alphanumeric string of a specified length.

    Parameters
    ----------
    string_length: int
        The length of the random string to return.
    """

    return "".join(
        random.choices(string.ascii_letters + string.digits, k=string_length)
    )


def stub_boto_client(
    service: str, method: str, response: dict, expected_parameters: dict
) -> boto3.client:
    """
    Stub a boto3 service interaction using the boto Stubber.

    Parameters
    ----------
    service: str
        The name of an AWS service to stub an interaction with, e.g. "s3" or "ssm".
    method: str
        The name of a boto3 method for the service to stub out, e.g. "get_parameter".
    response: dict
        A valid mock response for the specified interaction.
    expected_parameters: dict
        A set of valid parameters to configure the AWS interaction.
    """

    client = boto3.client(service)
    stubbed_client = Stubber(client)
    stubbed_client.add_response(method, response, expected_parameters)
    stubbed_client.activate()
    return client
