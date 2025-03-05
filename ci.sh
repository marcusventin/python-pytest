#!/bin/bash

set -e
echo -e "\033[1;32m**** BUILDING VIRTUAL ENVIRONMENT ****\033[0m"
python3 -m venv venv
source venv/bin/activate
echo -e "\033[1;32m**** INSTALLING LINT DEPENDENCIES ****\033[0m"
pip install --upgrade pip
python3 -m pip install -r ./code_quality/lint/requirements.txt
echo -e "\033[1;32m**** RUNNING RUFF LINT ****\033[0m"
ruff check --config ./code_quality/lint/pyproject.toml
echo -e "\033[1;32m**** INSTALLING PROJECT DEPENDENCIES ****\033[0m"
python3 -m pip install -r ./script/requirements.txt
echo -e "\033[1;32m**** INSTALLING TEST DEPENDENCIES ****\033[0m"
python3 -m pip install -r ./code_quality/tests/requirements/requirements.txt
echo -e "\033[1;32m**** RUNNING UNIT TESTS ****\033[0m"
coverage run -m pytest code_quality/tests/unit_tests/* --log-cli-level=info && coverage report --omit "code_quality/**/*" -m
if [[ $? -ne 0 ]]; then
    exit $?
fi
# echo -e "\033[1;32m**** DESTROYING TEST ENVIRONMENT ****\033[0m"
# deactivate
# rm -rf venv
echo -e "\033[1;32m**** TESTS COMPLETE ****\033[0m"