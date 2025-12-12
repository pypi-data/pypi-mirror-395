# tests/steps/test_file_connector_upload_steps.py
import os
import json
from pathlib import Path
import requests
import urllib3
import pytest
from pytest_bdd import scenarios, given, when, parsers, then
from dotenv import dotenv_values
import time
import pandas as pd
from pathlib import Path

scenarios("file_connector/file_connector.feature")

@pytest.fixture
def api_ctx():
    return {"payload": None, "response": None}

def _env_cfg():
    BASE_DIR = Path(__file__).resolve().parents[4]
    env_path = BASE_DIR / ".env"
    env = dotenv_values(str(env_path))

    org = env.get("ORGANIZATION") or os.getenv("ORGANIZATION")
    base_url = (env.get("OPENGATE_URL") or os.getenv("OPENGATE_URL") or "").rstrip("/")
    api_key = env.get("OPENGATE_API_KEY") or os.getenv("OPENGATE_API_KEY")
    jwt = env.get("JWT") or os.getenv("JWT")

    if not org:
        raise RuntimeError(f"You must define ORGANIZATION in {env_path} or env vars")
    if not base_url:
        raise RuntimeError("OPENGATE_URL not found in .env or environment")

    return {
        "ORGANIZATION": org,
        "OPENGATE_URL": base_url,
        "OPENGATE_API_KEY": api_key,
        "JWT": jwt,
        "OPENGATE_USER": env.get("OPENGATE_USER") or os.getenv("OPENGATE_USER"),
        "OPENGATE_PASSWORD": env.get("OPENGATE_PASSWORD") or os.getenv("OPENGATE_PASSWORD"),
    }

def _detect_content_type(file_path: str) -> str:
    fp = file_path.lower()
    if fp.endswith((".tar.gz", ".tgz")): return "application/gzip"
    if fp.endswith((".tar.bz2", ".tbz2")): return "application/x-bzip2"
    if fp.endswith(".tar"): return "application/x-tar"
    if fp.endswith(".zip"): return "application/zip"
    return "application/octet-stream"

def _normalize_table_to_list(raw: str) -> list[str]:
    files, seen, out = [], set(), []
    for line in (raw or "").splitlines():
        line = line.strip()
        if not line: continue
        if "|" in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            files.extend([p for p in parts if p])
        else:
            files.append(line)
    for f in files:
        if f and f not in seen:
            seen.add(f); out.append(f)
    return out

@given(parsers.parse("I prepare file upload payload with file: {files}"))
def given_prepare_upload_payload(api_ctx, files):
    # Busca los assets en opengate_data/test/utils
    assets_dir = Path(__file__).resolve().parents[4] / "opengate_data/test/utils"
    filenames = _normalize_table_to_list(files)
    if not filenames:
        raise RuntimeError("At least one file must be provided in the table.")

    resolved = []
    for name in filenames:
        p = (assets_dir / name).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Test asset not found: {p}")
        resolved.append(str(p))

    api_ctx["payload"] = {
        "local_files": resolved,
        "destiny_path": "/test",
        "overwrite": True,
    }

@when("I upload file to file connector for organization")
def when_upload_files(api_ctx):
    cfg = _env_cfg()
    org = cfg["ORGANIZATION"]
    url = f"{cfg['OPENGATE_URL'].rstrip('/')}/fileConnector/organizations/{org}/upload"

    headers = {"User-Agent": "pytest-bdd/og-data-py"}
    if cfg["OPENGATE_API_KEY"]:
        headers["X-ApiKey"] = cfg["OPENGATE_API_KEY"]
    elif cfg["JWT"]:
        headers["Authorization"] = f"Bearer {cfg['JWT']}"
    else:
        raise RuntimeError("Provide OPENGATE_API_KEY or JWT in .env or environment")

    auth = (cfg["OPENGATE_USER"], cfg["OPENGATE_PASSWORD"]) \
        if cfg["OPENGATE_USER"] and cfg["OPENGATE_PASSWORD"] else None

    payload = api_ctx.get("payload") or {}
    local_files = payload.get("local_files") or []
    destiny_path = payload.get("destiny_path") or "/"
    overwrite = bool(payload.get("overwrite", True))

    if not local_files:
        raise RuntimeError("No local files prepared. Did you run the Given step?")

    file_path = local_files[0]  # el backend espera un único archive
    ct = _detect_content_type(file_path)

    data = {"meta": json.dumps({"destinyPath": destiny_path, "overwriteFiles": overwrite})}
    files = {"file": (os.path.basename(file_path), open(file_path, "rb"), ct)}

    r = requests.post(url, headers=headers, data=data, files=files,
                      auth=auth, timeout=180, verify=False)

    try:
        files["file"][1].close()
    except Exception:
        pass

    api_ctx["response"] = {
        "status_code": r.status_code,
        "body": (r.json() if "application/json" in (r.headers.get("Content-Type") or "") else None),
        "text": r.text,
        "url": r.url,
    }


@given("I delete file from file connector for organization")
def given_delete_files(api_ctx):
    """
    Llama a POST /fileConnector/organizations/{org}/delete
    borrando la carpeta /test/ en el file connector.
    """
    cfg = _env_cfg()
    org = cfg["ORGANIZATION"]
    url = f"{cfg['OPENGATE_URL'].rstrip('/')}/fileConnector/organizations/{org}/delete"

    headers = {"User-Agent": "pytest-bdd/og-data-py"}
    if cfg["OPENGATE_API_KEY"]:
        headers["X-ApiKey"] = cfg["OPENGATE_API_KEY"]
    elif cfg["JWT"]:
        headers["Authorization"] = f"Bearer {cfg['JWT']}"
    else:
        raise RuntimeError("Provide OPENGATE_API_KEY or JWT in .env or environment")

    auth = (cfg["OPENGATE_USER"], cfg["OPENGATE_PASSWORD"]) \
        if cfg["OPENGATE_USER"] and cfg["OPENGATE_PASSWORD"] else None

    # Usa la misma ruta remota que empleaste en la subida
    payload = {"destinyPath": "/test/"}

    r = requests.post(
        url,
        headers=headers,
        json=payload,
        auth=auth,
        timeout=60,
        verify=False
    )

    api_ctx["response"] = {
        "status_code": r.status_code,
        "body": (r.json() if "application/json" in (r.headers.get("Content-Type") or "") else None),
        "text": r.text,
        "url": r.url,
    }

@given(parsers.parse('I want to use a destiny path "{path}"'))
def step_path(builder_holder, path):
    builder_holder["instance"].with_destiny_path(path)

@given(parsers.parse('I want to use find name "{find_name}"'))
def step_find_by_name(builder_holder, find_name):
    builder_holder["instance"].with_find_name(find_name)

@given(parsers.parse('I want to use add filename "{filename}"'))
def step_add_remote_file(builder_holder, filename):
    builder_holder["instance"].add_remote_file(filename)

@given(parsers.parse('I want to save the file to "{output_path}"'))
def step_save_file(builder_holder, output_path):
    builder_holder["instance"].with_output_path(output_path)

@given(parsers.parse('I want to add the local file to "{filename}"'))
def step_add_file(builder_holder, filename):
    builder_holder["instance"].add_local_file(filename)

@given(parsers.parse('I want to use a overwrite files'))
def step_find_by_name(builder_holder):
    builder_holder["instance"].with_overwrite_files(True)

@given(parsers.parse("I don't want a overwrite files"))
def step_find_by_name(builder_holder):
    builder_holder["instance"].with_overwrite_files(False)

@given("I prepare a dataframe to upload files")
def step_prepare_df_upload(builder_holder):
    base_dir = Path(__file__).resolve().parents[4]
    assets_dir = base_dir / "opengate_data/test/utils"

    zip_path = (assets_dir / "test_files.zip").resolve()
    tar_path = (assets_dir / "sample.tar").resolve()

    if not zip_path.exists():
        raise FileNotFoundError(zip_path)
    if not tar_path.exists():
        raise FileNotFoundError(tar_path)

    df_upload = pd.DataFrame([
        {"local_file": str(zip_path), "destiny_path": "/test/df_zip", "overwrite": True},
        {"local_file": str(tar_path), "destiny_path": "/test/df_tar", "overwrite": True},
    ])

    builder = builder_holder["instance"]
    builder.from_dataframe(df_upload)

@given("I prepare a dataframe to download files")
def step_prepare_df_download(builder_holder):
    df_download = pd.DataFrame([
        {
            "path": "/test/df_zip/multiples_ficheros",
            "filename": "upload.py",
            "output_path": "utils",
        },
        {
            "path": "/test/df_zip/multiples_ficheros",
            "filename": "show.py",
            "output_path": "utils",
        },
    ])

    builder = builder_holder["instance"]
    builder.from_dataframe(df_download)

@given("I prepare a dataframe to delete one file")
def step_prepare_df_delete_one(builder_holder):
    df_delete_one = pd.DataFrame([
        {"path": "/test/df_zip/multiples_ficheros", "filename": "upload.py"},
    ])

    builder = builder_holder["instance"]
    builder.from_dataframe(df_delete_one)

@given("I prepare a dataframe to delete paths")
def step_prepare_df_delete(builder_holder):
    df_delete = pd.DataFrame([
        {"path": "/test/df_zip", "filename": ""},
        {"path": "/test/df_tar", "filename": ""},
    ])

    builder = builder_holder["instance"]
    builder.from_dataframe(df_delete)

@given(parsers.re(r"^I want to add the local multiple files (?P<files>.+)$"))
def step_add_local_multiple_files(builder_holder, files: str):
    raw = files.strip().strip('"').strip("'")
    raw = raw.replace(" and ", ",")
    paths = [p.strip() for p in raw.split(",") if p.strip()]

    if not paths:
        raise RuntimeError("At least one local file must be provided")

    builder_holder["instance"].add_local_multiple_files(paths)


@when('I upload')
def step_upload(builder_holder):
    builder_holder["instance"].upload()
    time.sleep(2)

@when('I download')
def step_download(builder_holder):
    builder_holder["instance"].download()
    time.sleep(2)

@when('I list all files')
def step_list_all(builder_holder):
    builder_holder["instance"].list_all()
    time.sleep(2)

@when('I list all files')
def step_list_all(builder_holder):
    builder_holder["instance"].list_all()
    time.sleep(2)

@when('I list one file')
def step_list_one(builder_holder):
    builder_holder["instance"].list_one()
    time.sleep(2)


