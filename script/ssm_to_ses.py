"""
Pull a parameter from the SSM parameter store and send it in an email using Simple Email
Service.
"""

import logging
import os
import sys

import boto3
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main(recipient: str, parameter_names: list[str]) -> None:
    """
    Call a function to collect SSM parameters and email to a specified recipient.

    Parameters
    ----------
    recipient: str
        The email address to send parameter details to.
    parameter_names: list[str]
        A list of parameter names to collect from the SSM Parameter Store.
    """

    logger.info("FUNCTION STARTED")
    send_parameters(recipient, parameter_names)


def send_parameters(recipient: str, parameter_names: list[str]) -> None:
    """
    Get a parameter value from the SSM Parameter Store then send via Simple Email
    Service.

    Parameters
    ----------
    recipient: str
        The email address to send parameter details to.
    parameter_names: list[str]
        A list of parameter names to collect from the SSM Parameter Store.
    """

    parameter_details = get_parameter_values(parameter_names)
    email_parameters(recipient, parameter_details)


def get_parameter_values(
    parameter_names: list[str],
    client: boto3.client = None,
) -> list[dict[str]]:
    """
    Get a parameter value from the SSM Parameter Store.

    Parameters
    ----------
    parameter_names: list[str]
        A list of SSM parameter names to retrieve.
    client: boto3.client
        The Boto3 client to handle AWS interactions. Set in the function if not supplied
        as an argument.

    Returns
    -------
    dict[str]
        A list of dictionaries containing "name" and "value" keys that hold parameter
        details.
    """

    client = client if client else boto3.client("ssm")
    logger.info("Getting values of parameters %s", parameter_names)
    response = client.get_parameters(Names=parameter_names, WithDecryption=True)
    logger.debug("get_parameter response: %s", response)
    return [
        {"name": parameter["Name"], "value": parameter["Value"]}
        for parameter in response["Parameters"]
    ]


def email_parameters(recipient: str, parameters: list[dict[str]]) -> None:
    """
    Generate an email template containing a parameter value and send using SES.

    Parameters
    ----------
    recipient: str
        The email address to send parameter details to.
    parameters: list[dict[str]]
        A list of dictionaries containing parameter names and values.
    """

    templates = build_templates("ssm_to_ses", parameters)
    send_email(recipient, templates)


def build_templates(template_file: str, parameters: list[dict[str]]) -> dict[str]:
    """
    Build HTML and TXT email templates using Jinja2.

    Parameters
    ----------
    template_file: str
        The name of a template file. Must exist in the "templates" directory with txt
        and html extensions.
    parameters: list[dict[str]]
        A list of dictionaries containing names and values of parameters to insert into
        a template.
    """

    environment = get_environment()
    return {
        "txt": build_template(environment, f"{template_file}.txt", parameters),
        "html": build_template(environment, f"{template_file}.html", parameters),
    }


def get_environment() -> Environment:
    """
    Return a Jinja2 Environment pointed at a template directory.
    """

    return Environment(
        loader=FileSystemLoader(os.environ["TEMPLATE_PATH"]), autoescape=True
    )


def build_template(
    environment: Environment,
    template_file: str,
    parameters: list[dict[str]],
) -> str:
    """
    Render a template using Jinja2 and return as a string.

    Parameters
    ----------
    environment: jinja2.Environment
        A Jinja2 environment pointed at a directory containing template files.
    template_file: str
        The name of a file containing a Jinja2 template to be rendered.
    parameters: list[dict[str]]
        A list of dictionaries containing names and values of parameters to insert into
        a template.
    """

    template = environment.get_template(template_file)
    rendered_template = template.render(parameters=parameters)
    logger.debug("Rendered template: %s", rendered_template)
    return rendered_template


def send_email(
    recipient: str,
    templates: dict[str],
    client: boto3.client = None,
) -> dict:
    """
    Send an email to a recipient using AWS's Simple Email Service.

    Parameters
    ----------
    recipient: str
        The email address to send parameter details to.
    templates: dict[str]
        A dictionary containing txt and html email templates.
    client: boto3.client
        The Boto3 client to handle AWS interactions. Set in the function if not supplied
        as an argument.
    """

    client = client if client else boto3.client("ses")
    response = client.send_email(
        Source=os.environ["SENDER"],
        Destination={"ToAddresses": [recipient]},
        Message={
            "Subject": {"Data": "SSM Parameter Values", "Charset": "utf-8"},
            "Body": {
                "Text": {"Data": templates["txt"], "Charset": "utf-8"},
                "Html": {"Data": templates["html"], "Charset": "utf-8"},
            },
        },
    )
    logger.debug("Send email response: %s", response)
    return response


if __name__ == "__main__":
    recipient = sys.argv[1]
    parameter_names = sys.argv[2:]
    main(parameter_names)
