"""
Fixtures to facilitate the end-to-end testing of the ssm_to_ses script.
"""

import boto3
import pytest
from moto import mock_aws


@pytest.fixture(name="ssm_client")
def fixture_mock_ssm_client() -> boto3.client:
    """
    Return a mock SSM client.
    """

    with mock_aws():
        yield boto3.client("ssm")


@pytest.fixture(name="build_parameters")
def fixture_build_parameters(ssm_client, parameters) -> None:
    """
    Build mock SSM parameters using moto.
    """

    for parameter in parameters:
        ssm_client.put_parameter(
            Name=parameter["name"], Value=parameter["value"], Type="SecureString"
        )


@pytest.fixture(name="ses_client")
def fixture_mock_ses_client() -> boto3.client:
    """
    Return a mock SES client.
    """

    with mock_aws():
        yield boto3.client("ses")


@pytest.fixture(name="build_ses")
def fixture_mock_ses(ses_client, set_envs) -> None:
    """
    Build mock SES infrastructure.
    """

    ses_client.verify_email_identity(EmailAddress=set_envs["SENDER"])
