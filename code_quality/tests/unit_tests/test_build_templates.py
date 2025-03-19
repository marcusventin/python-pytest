"""
Unit tests for the "build_templates" function. Designed to be run from the project's top
level.
"""

from unittest.mock import call

from code_quality.tests.tools import random_string
from script.ssm_to_ses import build_templates


def test_returns_expected_values(mocker, ssm_to_ses, environment, parameters):
    """
    Does build_templates call expected functions with expected arguments, and return an
    expected response?
    """

    mock_get_environment = mocker.patch(
        f"{ssm_to_ses}.get_environment",
        return_value=environment,
    )
    txt_template = random_string(8)
    html_template = random_string(8)
    mock_build_template = mocker.patch(
        f"{ssm_to_ses}.build_template",
        side_effect=[txt_template, html_template],
    )
    mock_template_file = random_string(6)

    response = build_templates(mock_template_file, parameters)

    assert response["txt"] == txt_template
    assert response["html"] == html_template
    mock_get_environment.assert_called_once()
    mock_build_template.assert_has_calls(
        [
            call(environment, f"{mock_template_file}.txt", parameters),
            call(environment, f"{mock_template_file}.html", parameters),
        ],
    )
