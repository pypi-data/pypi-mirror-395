import os
from pathlib import Path
import requests
import pytest
from pytest_bdd import scenarios, given, parsers, when, then
import time
from dotenv import dotenv_values
import pandas as pd

scenarios("timeseries/timeseries.feature")

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
        "JWT": jwt,
    }

@pytest.fixture
def api_ctx():
    # añadimos sitio donde guardar el parquet
    return {"payload": None, "response": None, "dataset_identifier": None, "parquet_df": None}


@given(parsers.parse('I want use a with output file "{name}"'))
def step_ouput_file(builder_holder, name: str):
    builder_holder["instance"].with_output_file(name)
    time.sleep(2)


@when('I export')
def step_export(builder_holder):
    builder_holder["instance"].export()
    time.sleep(2)


@when('I export status')
def step_export_status(builder_holder):
    builder_holder["instance"].export_status()
    time.sleep(2)


@then(parsers.parse(
    'I download the exported parquet from fileconnector path "{remote_path}" '
    'into local file "{local_filename}"'
))
def step_download_exported_parquet(api_ctx,
                                   remote_path: str,
                                   local_filename: str):
    cfg = _env_cfg()

    org = cfg["ORGANIZATION"]
    base_url = (cfg.get("OPENGATE_URL") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("OPENGATE_URL not configured in .env")

    headers: dict[str, str] = {}
    api_key = cfg.get("OPENGATE_API_KEY")
    jwt = cfg.get("JWT")

    if api_key:
        headers["X-ApiKey"] = api_key
    elif jwt:
        headers["Authorization"] = f"Bearer {jwt}"
    else:
        raise RuntimeError("You must define OPENGATE_API_KEY or JWT in .env")

    download_url = f"{base_url}/fileConnector/organizations/{org}/download"

    resp = requests.get(
        download_url,
        headers=headers,
        params={"path": remote_path},
        verify=False,
        timeout=60,
    )

    assert resp.status_code == 200, (
        f"Unexpected status code when downloading file: {resp.status_code}, "
        f"body={resp.text!r}"
    )

    base_dir = Path(__file__).resolve().parents[4]
    local_dir = base_dir / "opengate_data" / "test" / "utils"
    local_dir.mkdir(parents=True, exist_ok=True)

    local_path = local_dir / local_filename

    with open(local_path, "wb") as f:
        f.write(resp.content)

    try:
        df = pd.read_parquet(local_path)
    except ImportError as exc:
        pytest.skip(
            "pyarrow o fastparquet son necesarios para leer ficheros parquet en los tests "
            f"(detalle: {exc})"
        )

    api_ctx["parquet_df"] = df

    delete_url = f"{base_url}/fileConnector/organizations/{org}/delete"

    remote_path_obj = Path(remote_path)
    destiny_path = str(remote_path_obj.parent).replace("\\", "/") or "."
    file_name = remote_path_obj.name

    payload = {
        "destinyPath": destiny_path,
        "fileName": file_name,
    }

    del_resp = requests.post(
        delete_url,
        headers=headers,
        json=payload,
        verify=False,
        timeout=60,
    )

    assert del_resp.status_code in (204, 404), (
        f"Unexpected delete status code: {del_resp.status_code}, "
        f"body={del_resp.text!r}"
    )

    try:
        local_path.unlink()
    except FileNotFoundError:
        pass

@then(parsers.parse(
    'the parquet must contain value "{expected_value}" in column "{column_name}"'
))
def step_parquet_must_contain_value_in_column(api_ctx,
                                              expected_value: str,
                                              column_name: str):
    df = api_ctx.get("parquet_df")
    assert df is not None, "parquet_df is not available in api_ctx; did you forget to download it first?"

    assert column_name in df.columns, (
        f"Column {column_name!r} not found in parquet columns: {list(df.columns)}"
    )

    series_str = df[column_name].astype(str)
    assert (series_str == str(expected_value)).any(), (
        f"Value {expected_value!r} not found in column {column_name!r}. "
        f"Data preview:\n{df.head()}"
    )


@then(parsers.parse(
    'the parquet column "{column_name}" must contain values "{values}"'
))
def step_parquet_column_must_contain_multiple_values(api_ctx,
                                                     column_name: str,
                                                     values: str):

    df = api_ctx.get("parquet_df")
    assert df is not None, "parquet_df is not available in api_ctx; did you forget to download it first?"

    assert column_name in df.columns, (
        f"Column {column_name!r} not found in parquet columns: {list(df.columns)}"
    )

    series_str = df[column_name].astype(str)

    expected_values = [v.strip() for v in values.split(",") if v.strip()]
    missing = [v for v in expected_values if not (series_str == v).any()]

    assert not missing, (
        f"Some expected values were not found in column {column_name!r}: {missing}. "
        f"Data preview:\n{df.head()}"
    )
