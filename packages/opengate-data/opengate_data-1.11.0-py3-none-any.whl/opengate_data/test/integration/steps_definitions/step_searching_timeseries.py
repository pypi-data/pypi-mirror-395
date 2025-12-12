import os
import json
import requests
import pytest
from dotenv import dotenv_values
from pytest_bdd import scenarios, given, when, then, parsers
import time

scenarios("searching/searching_timeseries.feature")

def _env_cfg():
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
    )
    env_path = os.path.join(BASE_DIR, ".env")
    return dotenv_values(env_path)

@pytest.fixture
def api_ctx():
    return {"payload": None, "response": None, "timeserie_identifier": None}



