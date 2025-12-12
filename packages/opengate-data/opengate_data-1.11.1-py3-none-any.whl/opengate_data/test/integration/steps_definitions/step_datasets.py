import os
import json
import requests
import pytest
from pytest_bdd import scenarios, given, parsers
import time

scenarios("datasets/find_datasets.feature")

@pytest.fixture
def api_ctx():
    return {"payload": None, "response": None, "dataset_identifier": None}

@given(parsers.parse('I find dataset by name "{dataset_name}"'))
def step_find_dataset_by_name(builder_holder, dataset_name: str):
    builder_holder["instance"].with_name(dataset_name)
    time.sleep(2)

@given(parsers.parse('I want a dataset name by environment variable "{env_name}"'))
def step_find_dataset_by_environment_variable_name(builder_holder, env_name: str):
    os.environ["DATASET"] = env_name
    builder_holder["instance"].with_env("DATASET", prefer="name")
    time.sleep(2)

