#!/bin/bash

LOG_LEVEL="debug"
PYPROJECT_PATH="./code_quality/pyproject.toml"
set -e
echo -e "\033[1;32m**** BUILDING VIRTUAL ENVIRONMENT ****\033[0m"
python3 -m venv venv
source venv/bin/activate
echo -e "\033[1;32m**** INSTALLING LINT DEPENDENCIES ****\033[0m"
pip install --upgrade pip
python3 -m pip install -r ./code_quality/lint/requirements.txt
echo -e "\033[1;32m**** RUNNING RUFF LINT ****\033[0m"
ruff check --config "${PYPROJECT_PATH}"
echo -e "\033[1;32m**** INSTALLING PROJECT DEPENDENCIES ****\033[0m"
python3 -m pip install -r ./script/requirements.txt
echo -e "\033[1;32m**** INSTALLING TEST DEPENDENCIES ****\033[0m"
python3 -m pip install -r ./code_quality/tests/requirements/requirements.txt
echo -e "\033[1;32m**** RUNNING UNIT TESTS ****\033[0m"
coverage run -m pytest -vv code_quality/tests/unit_tests/* --log-cli-level="${LOG_LEVEL}" && coverage report --omit "code_quality/**/*" --rcfile "${PYPROJECT_PATH}" -m
echo -e "\033[1;32m**** RUNNING INTEGRATION TESTS ****\033[0m"
coverage run -m pytest -vv code_quality/tests/integration_tests/* --log-cli-level="${LOG_LEVEL}"
echo -e "\033[1;32m**** INSTALLING END-TO-END TEST DEPENDENCIES ****\033[0m"
python3 -m pip install -r ./code_quality/tests/requirements/end_to_end/requirements.txt
echo -e "\033[1;32m**** RUNNING END-TO-END TESTS ****\033[0m"
coverage run -m pytest -vv code_quality/tests/end_to_end_tests/* --log-cli-level="${LOG_LEVEL}" && coverage report --omit "code_quality/**/*" --rcfile "${PYPROJECT_PATH}" -m
if [[ $? -ne 0 ]]; then
    exit $?
fi
# echo -e "\033[1;32m**** DESTROYING TEST ENVIRONMENT ****\033[0m"
# deactivate
# rm -rf venv
echo -e "\033[1;32m**** TESTS COMPLETE ****\033[0m"