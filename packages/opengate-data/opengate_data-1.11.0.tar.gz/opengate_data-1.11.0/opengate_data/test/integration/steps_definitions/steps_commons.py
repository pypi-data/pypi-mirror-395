import ast
import json
import time
from configparser import ConfigParser
import os
import pytest
import requests
from pytest_bdd import given, when, then, parsers
from pathlib import Path
from dotenv import dotenv_values
from typing import List

from opengate_data.utils.utils import send_request
from opengate_data.ai_models.ai_models import AIModelsBuilder
from opengate_data.ai_pipelines.ai_pipelines import AIPipelinesBuilder
from opengate_data.ai_transformers.ai_transformers import AITransformersBuilder
from opengate_data.rules.rules import RulesBuilder
from opengate_data.searching.builder.entities_search import EntitiesSearchBuilder
from opengate_data.searching.builder.datasets_search import DatasetsSearchBuilder
from opengate_data.searching.builder.timeseries_search import TimeseriesSearchBuilder
from opengate_data.searching.builder.datapoints_search import DataPointsSearchBuilder
from opengate_data.searching.builder.rules_search import RulesSearchBuilder as SearchingRulesBuilder
from opengate_data.collection.iot_collection import IotCollectionBuilder
from opengate_data.collection.iot_bulk_collection import IotBulkCollectionBuilder
from opengate_data.provision.bulk.provision_bulk import ProvisionBulkBuilder
from opengate_data.provision.asset.provision_asset import ProvisionAssetBuilder
from opengate_data.provision.devices.provision_device import ProvisionDeviceBuilder
from opengate_data.collection.iot_pandas_collection import PandasIotCollectionBuilder
from opengate_data.datasets.find_datasets import FindDatasetsBuilder
from opengate_data.timeseries.find_timeseries import FindTimeseriesBuilder
from opengate_data.timeseries.timeseries import TimeseriesBuilder
from opengate_data.file_connector.file_connector import FileConnectorBuilder

BUILDER_MAP = {
    "model": AIModelsBuilder,
    "transformer": AITransformersBuilder,
    "pipeline": AIPipelinesBuilder,
    "rule": RulesBuilder,
    "entity": EntitiesSearchBuilder,
    "dataset": DatasetsSearchBuilder,
    "timeserie": TimeseriesSearchBuilder,
    "datapoint": DataPointsSearchBuilder,
    "iot collection": IotCollectionBuilder,
    "iot bulk collection": IotBulkCollectionBuilder,
    "iot pandas collection": PandasIotCollectionBuilder, 
    "provision bulk": ProvisionBulkBuilder,
    "searching rules": SearchingRulesBuilder,
    "provision asset": ProvisionAssetBuilder,
    "provision device": ProvisionDeviceBuilder,
    "find datasets": FindDatasetsBuilder,
    "find timeseries": FindTimeseriesBuilder,
    "timeseries": TimeseriesBuilder,
    "file connector": FileConnectorBuilder
}

# --- Cleanup automatic ---
@pytest.fixture(scope="module")
def _created_devices_registry():
    return set()

@pytest.fixture
def api_ctx():
    return {"response": None}

def _env_cfg():
    BASE_DIR = Path(__file__).resolve().parents[4]
    env_path = BASE_DIR / ".env"
    env = dotenv_values(str(env_path))

    org = env.get("ORGANIZATION")
    channel = env.get("CHANNEL", "default_channel")
    service_group = env.get("SERVICE_GROUP", "emptyServiceGroup")
    url = env.get("OPENGATE_URL")
    api_key = env.get("OPENGATE_API_KEY")
    jwt = env.get("JWT")
    if not org:
        raise RuntimeError(f"You must define ORGANIZATION in {env_path}")

    return {
        "ORGANIZATION": org,
        "CHANNEL": channel,
        "SERVICE_GROUP": service_group,
        "OPENGATE_URL": url,
        "OPENGATE_API_KEY": api_key,
        "JWT": jwt
    }

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]

def _resolve_test_path(p: str | os.PathLike) -> Path:
    p = Path(p)
    if p.is_absolute():
        return p
    return _repo_root() / p

def _ensure_ini_section(config_file: str, section: str, key: str):
    cfg_path = _resolve_test_path(config_file)
    cfg_path.parent.mkdir(parents=True, exist_ok=True)

    cp = ConfigParser()
    if cfg_path.exists():
        cp.read(cfg_path)
    if not cp.has_section(section):
        cp.add_section(section)
    if not cp.has_option(section, key):
        cp.set(section, key, "")

    with cfg_path.open("w") as f:
        cp.write(f)

def _parse_ids(ids_literal: str) -> List[str]:
    ids_str = ids_literal.strip()
    if ids_str.startswith("["):
        import json
        return json.loads(ids_str)
    return [s.strip().strip('"').strip("'") for s in ids_str.split(",") if s.strip()]


def _create_device(client, org, channel, service_group, device_id):
    url = f"{client.url}/north/v80/provision/organizations/{org}/devices?flattened=true"
    payload = {
        "provision.device.identifier": {"_value": {"_current": {"value": device_id}}},
        "provision.administration.organization": {"_value": {"_current": {"value": org}}},
        "provision.administration.channel": {"_value": {"_current": {"value": channel}}},
        "provision.administration.serviceGroup": {"_value": {"_current": {"value": service_group}}},
        "provision.device.software": {"_value": {"_current": {"value": []}}},
        "provision.device.serialNumber": {"_value": {"_current": {"value": "123456"}}},

    }
    headers = {**client.headers, "Accept": "application/json", "Content-Type": "application/json"}
    resp = send_request(method="post", headers=headers, url=url, json_payload=payload)

    if resp.status_code in (200, 201, 409):
        return

    try:
        body = resp.json()
    except Exception:
        body = {}

    msg = str(body) if body else resp.text
    if resp.status_code == 400 and ("Entity duplicated" in msg or "0x010114" in msg):
        return

    raise AssertionError(f"Create {device_id} failed: HTTP {resp.status_code} - {resp.text}")

    
def _delete_device(client, org: str, device_id: str):
    url = f"{client.url}/north/v80/provision/organizations/{org}/devices/{device_id}?flattened=true"
    headers = dict(client.headers or {})
    headers.pop("Accept", None)
    headers["Accept"] = "*/*"

    resp = send_request(method="delete", headers=headers, url=url)
    if resp.status_code not in (200, 204, 404):
        raise AssertionError(f"Delete {device_id} failed: HTTP {resp.status_code} - {resp.text}")


def _split_csv_paths(raw: str) -> list[str]:
    return [p.strip() for p in (raw or "").split(",") if p.strip()]

# --- Fixture to store the active builder ---
@pytest.fixture
def builder_holder():
    """Holds the current builder instance across steps."""
    return {"instance": None}


# ------Given ------

@given(parsers.parse('I want to build a "{build_type}"'))
def step_build(client, builder_holder, build_type):
    builder_cls = BUILDER_MAP.get(build_type)
    if not builder_cls:
        raise ValueError(f"Unknown builder type: {build_type}")
    builder_holder["instance"] = builder_cls(client)

@given(parsers.parse('I want to use a select {select}'))
def step_prediction_result(builder_holder, select):
    select = select.replace("'", '"')
    select_list = json.loads(select)
    builder_holder["instance"].with_select(select_list)

@given(parsers.parse('I want to use a limit {start}, {size}'))
def step_prediction_result(builder_holder, start, size):
    builder_holder["instance"].with_limit(start, size)

@given(parsers.re(r'^I want to use a filter\s+(?P<filter_data>.+)$'))
def step_with_filter(builder_holder, filter_data: str):
    s = filter_data.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1]
    data = ast.literal_eval(s)
    builder_holder["instance"].with_filter(data)

@given(parsers.parse('I want to use a limit {select}'))
def step_prediction_result(builder_holder, select):
    select = select.replace("'", '"')
    select_list = json.loads(select)
    builder_holder["instance"].with_select(select_list)

@given(parsers.parse('I want to use a format "{format_path}"'))
def step_with_format(builder_holder, format_path):
    builder_holder["instance"].with_format(format_path)

@given(parsers.parse('I want to use organization'))
def step_organization(builder_holder):
    org = _env_cfg()['ORGANIZATION']
    builder_holder["instance"].with_organization_name(org)

@given(parsers.parse('I want to use a channel'))
def step_with_channel(builder_holder):
    channel = _env_cfg()['CHANNEL']
    builder_holder["instance"].with_channel(channel)

@given(parsers.parse('I want to use a name "{name}"'))
def step_with_name(builder_holder, name):
    builder_holder["instance"].with_name(name)

@given('I want to use a active rule as False')
def step_rule_activate_false(builder_holder):
    builder_holder["instance"].with_active(False)

@given(parsers.parse('I want to search by name "{name}"'))
def step_search_by_name(builder_holder, name):
    builder_holder["instance"].with_find_by_name(name)

@given(parsers.parse('I want to use a mode "{mode}"'))
def step_with_mode(builder_holder, mode):
    builder_holder["instance"].with_mode(mode)

@given(parsers.parse('I want to use a type "{type_data}"'))
def step_with_type(builder_holder, type_data):
    builder_holder["instance"].with_type(ast.literal_eval(type_data))

@given(parsers.parse('I want to use a condition "{condition}"'))
def step_with_condition(builder_holder, condition):
    builder_holder["instance"].with_condition(ast.literal_eval(condition))

@given(parsers.parse('I want to use a actions delay {actions_delay}'))
def step_with_actions_delay(builder_holder, actions_delay):
    builder_holder["instance"].with_actions_delay(1000)

@given(parsers.parse('I want to use a actions "{actions}"'))
def step_with_actions(builder_holder, actions):
    builder_holder["instance"].with_actions(ast.literal_eval(actions))

@given(parsers.parse('I want to search id in a configuration file "{config_file}" "{section}" "{config_key}"'))
def step_search_id_config_file(builder_holder, config_file, section, config_key):
    cfg_path = _resolve_test_path(config_file)
    builder_holder["instance"].with_config_file(str(cfg_path), section, config_key)
    time.sleep(2)

@given(parsers.parse('I want to save id in a configuration file "{config_file}" "{section}" "{config_key}"'))
def step_set_id_config_file(builder_holder, config_file, section, config_key):
    cfg_path = _resolve_test_path(config_file)
    _ensure_ini_section(str(cfg_path), section, config_key)
    builder_holder["instance"].with_config_file(str(cfg_path), section, config_key)
    time.sleep(2)

@given(parsers.parse('I ensure test devices exist: {ids}'))
def ensure_test_devices(client, _created_devices_registry, ids):
    """
    Deletes if it exists (ignores 404) and creates it afterward. Doesn't fail if it didn't exist.
    Logs for deletion at the end of the module.
    """
    cfg = _env_cfg()
    org = cfg["ORGANIZATION"]
    ch = cfg["CHANNEL"]
    sg = cfg["SERVICE_GROUP"]

    for dev in _parse_ids(ids):
        try:
            _delete_device(client, org, dev)
        except AssertionError:
            pass
        _create_device(client, org, ch, sg, dev)
        _created_devices_registry.add(dev)

@given(parsers.parse('I ensure test devices delete: "{device_id}"'))
def delete_device(client, device_id):
    cfg = _env_cfg()
    org = cfg["ORGANIZATION"]

    url = f"{client.url}/north/v80/provision/organizations/{org}/devices/{device_id}?flattened=true"

    headers = dict(client.headers or {})
    headers.pop("Accept", None)
    headers["Accept"] = "*/*"

    resp = send_request(method="delete", headers=headers, url=url)
    if resp.status_code not in (200, 204, 404):
        raise AssertionError(f"Delete {device_id} failed: HTTP {resp.status_code} - {resp.text}")

@given("I prepare a dataset payload:")
def step_prepare_dataset_payload(api_ctx, docstring):
    api_ctx["payload"] = json.loads(docstring)

@given(parsers.parse('I delete device if exists {ids}'))
def ensure_test_devices(client, ids):
    """
    Deletes if it exists (ignores 404) and creates it afterward. Doesn't fail if it didn't exist.
    Logs for deletion at the end of the module.
    """
    cfg = _env_cfg()
    org = cfg["ORGANIZATION"]

    for dev in _parse_ids(ids):
        try:
            _delete_device(client, org, dev)
        except AssertionError:
            pass

@given(parsers.parse('I search for timeserie by name "{timeserie_name}"'))
def step_search_timeserie_by_name(api_ctx, builder_holder, timeserie_name: str):
    cfg = _env_cfg()
    org = cfg.get("ORGANIZATION") or os.getenv("ORGANIZATION")
    if not org:
        raise RuntimeError("Key 'ORGANIZATION' not found in .env or environment")

    base_url = (cfg.get("OPENGATE_URL") or os.getenv("OPENGATE_URL") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("OPENGATE_URL not found in .env or environment")
    if "/north/" not in base_url.lower():
        base_url += "/north/v80"

    url = f"{base_url}/timeseries/provision/organizations/{org}"

    api_key = cfg.get("OPENGATE_API_KEY") or os.getenv("OPENGATE_API_KEY")
    jwt_token = cfg.get("JWT") or os.getenv("JWT")

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-ApiKey"] = api_key
    elif jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"
    else:
        raise RuntimeError("Provide OPENGATE_API_KEY or JWT")

    r = requests.get(url, headers=headers, verify=False, timeout=30)
    data = r.json() if "application/json" in (r.headers.get("Content-Type") or "") else {}
    lst = data.get("timeseries") or data.get("items") or []
    match = next((t for t in lst if t.get("name") == timeserie_name), None)
    if not match:
        raise RuntimeError(f"Timeserie with name {timeserie_name} not found")
    identifier = match["identifier"]
    api_ctx["timeserie_identifier"] = identifier

    if builder_holder.get("instance"):
        builder_holder["instance"].with_identifier(identifier)


@when('I provision the dataset for organization')
def step_post_dataset(api_ctx):
    cfg = _env_cfg()

    org = cfg.get("ORGANIZATION") or os.getenv("ORGANIZATION")
    if not org:
        raise RuntimeError("Key 'ORGANIZATION' not found in .env or environment")

    base_url = (cfg.get("OPENGATE_URL") or os.getenv("OPENGATE_URL") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("OPENGATE_URL not found in .env or environment")
    if "/north/" not in base_url.lower():
        base_url += "/north/v80"

    url_base = f"{base_url}/datasets/provision/organizations/{org}"
    payload = api_ctx["payload"]

    api_key = cfg.get("OPENGATE_API_KEY") or os.getenv("OPENGATE_API_KEY")
    jwt_token = cfg.get("JWT") or os.getenv("JWT")

    headers = {"Content-Type": "application/json", "User-Agent": "pytest-bdd/og-data-py"}
    if api_key:
        headers["X-ApiKey"] = api_key
    elif jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"
    else:
        raise RuntimeError("Provide OPENGATE_API_KEY or JWT in .env or environment")

    user = cfg.get("OPENGATE_USER") or os.getenv("OPENGATE_USER")
    password = cfg.get("OPENGATE_PASSWORD") or os.getenv("OPENGATE_PASSWORD")
    auth = (user, password) if user and password else None

    try:
        r_list = requests.get(url_base, headers=headers, verify=False, timeout=30)
        if "application/json" in (r_list.headers.get("Content-Type") or ""):
            data = r_list.json()
            existing = next((t for t in (data.get("datasets") or data.get("items") or [])
                             if t.get("name") == payload.get("name")), None)
            if existing and existing.get("identifier"):
                del_url = f"{url_base}/{existing['identifier']}"
                requests.delete(del_url, headers=headers, verify=False, timeout=30)
    except Exception:
        pass

    r = requests.post(url_base, json=payload, headers=headers, auth=auth, verify=False, timeout=30)

    api_ctx["response"] = {
        "status_code": r.status_code,
        "body": (r.json() if "application/json" in (r.headers.get("Content-Type") or "") else None),
        "text": r.text,
        "url": r.url,
    }


@given(parsers.parse('I search for dataset by name "{dataset_name}"'))
def step_search_dataset_by_name(api_ctx, builder_holder, dataset_name: str):
    cfg = _env_cfg()
    org = cfg.get("ORGANIZATION") or os.getenv("ORGANIZATION")
    if not org:
        raise RuntimeError("Key 'ORGANIZATION' not found in .env or environment")

    base_url = (cfg.get("OPENGATE_URL") or os.getenv("OPENGATE_URL") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("OPENGATE_URL not found in .env or environment")
    if "/north/" not in base_url.lower():
        base_url += "/north/v80"

    url = f"{base_url}/datasets/provision/organizations/{org}"

    api_key = cfg.get("OPENGATE_API_KEY") or os.getenv("OPENGATE_API_KEY")
    jwt_token = cfg.get("JWT") or os.getenv("JWT")

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-ApiKey"] = api_key
    elif jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"
    else:
        raise RuntimeError("Provide OPENGATE_API_KEY or JWT")

    r = requests.get(url, headers=headers, verify=False, timeout=30)
    data = r.json() if "application/json" in (r.headers.get("Content-Type") or "") else {}
    lst = data.get("datasets") or data.get("items") or []
    match = next((t for t in lst if t.get("name") == dataset_name), None)
    if not match:
        raise RuntimeError(f"dataset with name {dataset_name} not found")
    identifier = match["identifier"]
    api_ctx["dataset_identifier"] = identifier

    if builder_holder.get("instance"):
        builder_holder["instance"].with_identifier(identifier)

@given("I prepare a timeserie payload:")
def step_prepare_timeserie_payload(api_ctx, docstring):
    api_ctx["payload"] = json.loads(docstring)


# ------When ------

@when("I delete the timeserie")
def step_delete_timeserie(api_ctx):
    cfg = _env_cfg()
    org = cfg.get("ORGANIZATION") or os.getenv("ORGANIZATION")
    if not org:
        raise RuntimeError("Key 'ORGANIZATION' not found in .env or environment")

    base_url = (cfg.get("OPENGATE_URL") or os.getenv("OPENGATE_URL") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("OPENGATE_URL not found in .env or environment")
    if "/north/" not in base_url.lower():
        base_url += "/north/v80"

    identifier = api_ctx.get("timeserie_identifier")
    if not identifier:
        raise RuntimeError("Timeserie identifier not set in context (run the search step first)")

    url = f"{base_url}/timeseries/provision/organizations/{org}/{identifier}"

    api_key = cfg.get("OPENGATE_API_KEY") or os.getenv("OPENGATE_API_KEY")
    jwt_token = cfg.get("JWT") or os.getenv("JWT")

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-ApiKey"] = api_key
    elif jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"

    r = requests.delete(url, headers=headers, verify=False, timeout=30)

    api_ctx["response"] = {
        "status_code": r.status_code,
        "body": (r.json() if "application/json" in (r.headers.get("Content-Type") or "") else None),
        "text": r.text,
        "url": r.url,
    }

@when('I provision the timeserie for organization')
def step_post_timeserie(api_ctx):
    cfg = _env_cfg()

    org = cfg.get("ORGANIZATION") or os.getenv("ORGANIZATION")
    if not org:
        raise RuntimeError("Key 'ORGANIZATION' not found in .env or environment")

    base_url = (cfg.get("OPENGATE_URL") or os.getenv("OPENGATE_URL") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("OPENGATE_URL not found in .env or environment")
    if "/north/" not in base_url.lower():
        base_url += "/north/v80"

    url_base = f"{base_url}/timeseries/provision/organizations/{org}"
    payload = api_ctx["payload"]

    api_key = cfg.get("OPENGATE_API_KEY") or os.getenv("OPENGATE_API_KEY")
    jwt_token = cfg.get("JWT") or os.getenv("JWT")

    headers = {"Content-Type": "application/json", "User-Agent": "pytest-bdd/og-data-py"}
    if api_key:
        headers["X-ApiKey"] = api_key
    elif jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"
    else:
        raise RuntimeError("Provide OPENGATE_API_KEY or JWT in .env or environment")

    user = cfg.get("OPENGATE_USER") or os.getenv("OPENGATE_USER")
    password = cfg.get("OPENGATE_PASSWORD") or os.getenv("OPENGATE_PASSWORD")
    auth = (user, password) if user and password else None

    try:
        r_list = requests.get(url_base, headers=headers, verify=False, timeout=30)
        if "application/json" in (r_list.headers.get("Content-Type") or ""):
            data = r_list.json()
            existing = next((t for t in (data.get("timeseries") or data.get("items") or [])
                             if t.get("name") == payload.get("name")), None)
            if existing and existing.get("identifier"):
                del_url = f"{url_base}/{existing['identifier']}"
                requests.delete(del_url, headers=headers, verify=False, timeout=30)
    except Exception:
        pass

    r = requests.post(url_base, json=payload, headers=headers, auth=auth, verify=False, timeout=30)

    api_ctx["response"] = {
        "status_code": r.status_code,
        "body": (r.json() if "application/json" in (r.headers.get("Content-Type") or "") else None),
        "text": r.text,
        "url": r.url,
    }    

@when('I create')
def step_create(builder_holder):
    builder_holder["instance"].create()
    time.sleep(2)

@when('I search')
def step_search(builder_holder):
    builder_holder["instance"].search()
    time.sleep(2)

@when('I delete')
def step_delete(builder_holder):
    builder_holder["instance"].delete()
    time.sleep(2)

@when('I update')
def step_update(builder_holder):
    builder_holder["instance"].update()
    time.sleep(2)

@when('I find one')
def step_find_one(builder_holder):
    builder_holder["instance"].find_one()
    time.sleep(2)

@when('I find all')
def step_find_all(builder_holder):
     builder_holder["instance"].find_all()
     time.sleep(2)
    
@when(parsers.parse('I collect IoT for device "{device_id}" with payload:'))
def when_collect_iot(api_ctx, device_id: str, docstring: str):
    cfg = _env_cfg()

    base_url = (cfg.get("OPENGATE_URL") or os.getenv("OPENGATE_URL") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("OPENGATE_URL not found in .env or environment")

    if "/south/" not in base_url.lower():
        base_url = f"{base_url}/south/v80"

    api_key = cfg.get("OPENGATE_API_KEY") or os.getenv("OPENGATE_API_KEY")
    if not api_key:
        raise RuntimeError("OPENGATE_API_KEY not found in .env or environment")

    url = f"{base_url}/devices/{device_id}/collect/iot"
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "X-ApiKey": api_key,
        "User-Agent": "pytest-bdd/og-data-py",
    }

    try:
        payload = json.loads(docstring)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON payload in feature docstring: {e}") from e

    r = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)

    api_ctx["response"] = {
        "status_code": r.status_code,
        "body": (r.json() if "application/json" in (r.headers.get("Content-Type") or "") else None),
        "text": r.text,
        "url": r.url,
    }

@when("I delete the dataset")
def step_delete_dataset(api_ctx):
    cfg = _env_cfg()
    org = cfg.get("ORGANIZATION") or os.getenv("ORGANIZATION")
    if not org:
        raise RuntimeError("Key 'ORGANIZATION' not found in .env or environment")

    base_url = (cfg.get("OPENGATE_URL") or os.getenv("OPENGATE_URL") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("OPENGATE_URL not found in .env or environment")
    if "/north/" not in base_url.lower():
        base_url += "/north/v80"

    identifier = api_ctx.get("dataset_identifier")
    if not identifier:
        raise RuntimeError("dataset identifier not set in context (run the search step first)")

    url = f"{base_url}/datasets/provision/organizations/{org}/{identifier}"

    api_key = cfg.get("OPENGATE_API_KEY") or os.getenv("OPENGATE_API_KEY")
    jwt_token = cfg.get("JWT") or os.getenv("JWT")

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-ApiKey"] = api_key
    elif jwt_token:
        headers["Authorization"] = f"Bearer {jwt_token}"

    r = requests.delete(url, headers=headers, verify=False, timeout=30)

    api_ctx["response"] = {
        "status_code": r.status_code,
        "body": (r.json() if "application/json" in (r.headers.get("Content-Type") or "") else None),
        "text": r.text,
        "url": r.url,
    }

@then(parsers.parse('I remove files in local "{files}"'))
def then_remove_files_csv(files: str):
    errors = []
    for p in _split_csv_paths(files):
        try:
            os.remove(p)
        except FileNotFoundError:
            errors.append(f"Not found: {p}")
        except IsADirectoryError:
            errors.append(f"Is a directory (not removed): {p}")
        except Exception as e:
            errors.append(f"{p}: {e}")
    if errors:
        raise RuntimeError("Cannot remove some files:\n- " + "\n- ".join(errors))

# ------Then ------
@then(parsers.parse("The HTTP status should be {code:d}"))
def step_check_status(api_ctx, code: int):
    assert api_ctx["response"] and api_ctx["response"]["status_code"] == code, \
        f"Expected {code}, got {api_ctx['response']}"
    time.sleep(2)
    
@then(parsers.parse('The status code from collection should be "{status_code}"'))
def then_collection_status_code(builder_holder, status_code):
    resp = builder_holder["instance"].build().execute()
    assert isinstance(resp, dict)
    assert "status_code" in resp
    assert resp["status_code"] == int(status_code)

@then(parsers.parse('The response should be "{status_code}"'))
def step_status_code(builder_holder, status_code):
    response = builder_holder["instance"].build().execute()
    print("Response received:", response)
    assert response["status_code"] == int(status_code)

@then(parsers.parse('The response search should be "{expected_type}"'))
def step_response_type(builder_holder, expected_type):
    raw = builder_holder["instance"].build().execute()
    payload = raw.get("response", raw) if isinstance(raw, dict) else raw

    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            pass

    if expected_type == "dict":
        assert isinstance(payload, dict)
    elif expected_type == "csv":
        assert isinstance(payload, str)
    elif expected_type == "pandas":
        import pandas as pd
        assert isinstance(payload, pd.DataFrame)
    else:
        raise ValueError(f"Unsupported expected_type: {expected_type}")
    
@then(parsers.parse('The response search should be "{expected_type}" and status code {expected_status_code:d}'))
def then_response_type_and_status(builder_holder, expected_type: str, expected_status_code: int):
    def derive_status(r):
        if isinstance(r, dict) and "status_code" in r:
            return r["status_code"]
        if isinstance(r, dict) and isinstance(r.get("results"), list):
            statuses = [item.get("status_code", 500) for item in r["results"]]
            if not statuses:
                return None
            return 200 if all(s == 200 for s in statuses) else next(s for s in statuses if s != 200)
        return None

    resp = builder_holder["instance"].build().execute()
    builder_holder["last_response"] = resp

    status = derive_status(resp)
    assert status is not None, f"Could not determine status_code from response: {resp!r}"
    assert status == expected_status_code, f"Expected {expected_status_code}, got {status}; response={resp!r}"

    if expected_type == "dict":
        assert isinstance(resp, dict), f"Expected dict, got {type(resp)}; response={resp!r}"
    elif expected_type == "pandas":
        import pandas as pd
        assert isinstance(resp, pd.DataFrame), f"Expected pandas DataFrame, got {type(resp)}"
    elif expected_type == "csv":
        assert isinstance(resp, str), f"Expected CSV string, got {type(resp)}"
    else:
        raise ValueError(f"Unsupported expected_type: {expected_type}")

@then(parsers.parse('The export status should be "{expected_status}"'))
def then_export_status(builder_holder, expected_status: str):
    resp = builder_holder.get("last_response")

    if resp is None:
        resp = builder_holder["instance"].build().execute()
        builder_holder["last_response"] = resp

    assert isinstance(resp, dict), f"Expected dict response, got {type(resp)}: {resp!r}"

    data = resp.get("data")
    assert isinstance(data, dict), f"Expected 'data' dict in response, got {type(data)}: {resp!r}"

    status = data.get("status")
    assert status == expected_status, (
        f"Expected export status '{expected_status}', got '{status}'; response={resp!r}"
    )
