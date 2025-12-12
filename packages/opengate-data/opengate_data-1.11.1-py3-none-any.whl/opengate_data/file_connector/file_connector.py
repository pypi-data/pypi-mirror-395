from requests import Response
from opengate_data.utils.utils import (
    validate_type, validate_build, send_request, set_method_call,parse_json,
)
import pandas as pd
import os
import json

class FileConnectorBuilder():
    """ File Connector Builder """

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.base_url = f'{self.client.url}/' if self.client.url else 'https://file-connector:443'
        self.organization_name: str | None = None
        self.local_file = {"paths_files": []}
        self.filename   = {"files": []}
        self.path: str | None = None
        self.find_file_name: str | None = None
        self.overwrite_files: bool | None = None
        self.output_path: str | None = None
        self.format_data: str | None = None
        self.df: pd.DataFrame | None = None
        self.df_defaults: dict | None = None
        self.method: str | None = None
        self.method_calls: list = []

    @set_method_call
    def with_organization_name(self, organization_name: str) -> 'FileConnectorBuilder':
        """
        Set organization name

        Args:
            organization_name (str):

        Returns:
            DatasetsSearchBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_organization_name("organization_name")
            ~~~
        """
        validate_type(organization_name, str, "Organization")
        self.organization_name = organization_name
        return self

    @set_method_call
    def with_overwrite_files(self, overwrite_files: bool) -> 'FileConnectorBuilder':
        """
        Set the overwrite file.

        Args:
            overwrite_files (bool):

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.
        """
        validate_type(overwrite_files, bool, "overwrite file")
        self.overwrite_files = overwrite_files
        return self

    @set_method_call
    def add_local_file(self, local_file: str) -> 'FileConnectorBuilder':
        """
        Add a single local file to be uploaded.

        You can call this method multiple times or combine it with
        `add_local_multiple_files()`.

        Args:
            local_file (str): Local file path to be uploaded.

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.add_local_file("data/file1.csv")
            ~~~
        """
        validate_type(local_file, str, "Local Path File")
        self.local_file["paths_files"].append(local_file)
        return self
    
    @set_method_call
    def add_local_multiple_files(self, local_files: list[str]) -> "FileConnectorBuilder":
        """
        Add multiple local files to be uploaded.

        The provided list can include one or more filesystem paths. They will be
        appended to the same internal collection used by `add_local_file`, so you
        can freely combine both methods:

            builder.add_local_file("foo.zip").add_local_multiple_files(["bar.zip", "baz.tar"])

        Args:
            local_files (list[str]): List of file paths to upload.

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.
        """
        validate_type(local_files, list, "Local Multiple Paths Files")
        for lf in local_files:
            validate_type(lf, str, "Local Path File")
            self.local_file["paths_files"].append(lf)
        return self


    def with_format(self, format_data: str) -> 'FileConnectorBuilder':
        """
        Formats the flat entities data based on the specified format ('dict', or 'pandas'). By default, the data is returned as a dictionary.

        Args:
            format_data (str): The format to use for the data.

        Example:
            builder.with_format('dict')
            builder.with_format('pandas')

        Returns:
            SearchBuilderBase: Returns itself to allow for method chaining.
        """
        validate_type(format_data, str, "Format")
        self.format_data = format_data
        return self

    @set_method_call
    def with_destiny_path(self, path: str) -> 'FileConnectorBuilder':
        """
        Set destiny path

        Args:
            path (str): 

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_destiny_path("path")
            ~~~
        """
        validate_type(path, str, "Destiny path")
        if path and not path.endswith("/"):
            path += "/"
        self.path = path
        return self

    @set_method_call
    def with_find_name(self, find_file_name: str) -> 'FileConnectorBuilder':
        """
        Set find by name

        Args:
            find_file_name (str): 

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_find_file_name("find_file_name")
            ~~
        """
        validate_type(find_file_name, str, "File Name")
        self.find_file_name = find_file_name
        return self

    @set_method_call
    def with_output_path(self, output_path: str) -> 'FileConnectorBuilder':
        """
        Set output path so that when downloading the file it is saved in that path
        Args:
            output_path (str): 

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_output_path("output_path")
            ~~~
        """
        validate_type(output_path, str, "Output Path")
        if output_path and not output_path.endswith("/"):
            output_path += "/"
        self.output_path = output_path
        return self

    @set_method_call
    def add_remote_file(self, file: str) -> 'FileConnectorBuilder':
        """
        Set remote filename

        Args:
            filename (str): 

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.add_remote_file("filename")
            ~~~
        """
        validate_type(file, str, "Remote Filename")
        self.filename["files"].append(file)
        return self

    @set_method_call
    def add_remote_multiple_files(self, files: list) -> 'FileConnectorBuilder':
        """
        Set remote multiples filenames

        Args:
            filename (str): 

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.add_remote_file("filename")
            ~~~
        """
        validate_type(files, list, "Remote Filenames")
        for file in files:
            validate_type(file, str, "Remote Filename")
            self.filename["files"].append(file)
        return self

    @set_method_call
    def from_dataframe(self, df: "pd.DataFrame", *, defaults: dict | None = None) -> 'FileConnectorBuilder':
        """
        Assign a DataFrame that describes operations per row.
        Expected columns (depending on method):
          - upload: local_file [req], destiny_path [opt], ​​overwrite [opt]
                       * If there is no destiny_path, use defaults['destiny_path'] or defaults['path'] or with_destiny_path(...) or "/"
                       * default overwrite = False
          - download: path [req], filename [req], output_path [opt]
                       * path can come from column, defaults['path'], with_destiny_path(...)
          - delete: path [req], filename [opt] (empty or absent -> delete the entire path)

        Supported defaults:
            {"destiny_path": str, "path": str, "overwrite": bool, "output_path": str}

        NOTE: if you mix from_dataframe with setters in download (path/filenames/output_path),
        then you must use all THREE setters; if not, use only from_dataframe.
 
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("from_dataframe(df): df debe ser un pandas.DataFrame")
        self.df = df.copy()
        self.df_defaults = defaults.copy() if isinstance(defaults, dict) else {}
        return self

    @set_method_call
    def upload(self) -> 'FileConnectorBuilder':
        """
        Configures the builder to upload a file to the specified organization.

        This method sets the internal state of the builder to prepare for a file upload operation. It does not execute the operation immediately but prepares the necessary configurations for when the `execute` method is called.

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.
        Example:
            ~~~python
                builder.upload()
            ~~~
        """
        self.method = 'upload'
        return self

    @set_method_call
    def list_all(self) -> 'FileConnectorBuilder':
        """
        Configures the builder to list files available in the specified organization.

        This method sets the internal state of the builder to prepare for a file listing operation. It does not execute the operation immediately but prepares the necessary configurations for when the `execute` method is called.

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.list_all()
            ~~~
        """
        self.method = 'list_all'
        return self

    @set_method_call
    def list_one(self) -> 'FileConnectorBuilder':
        """
        Configures the builder to list a single file from the specified organization.

        This method sets the internal state of the builder to prepare for a single file listing operation. It does not execute the operation immediately but prepares the necessary configurations for when the `execute` method is called.

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining.
        Example:
            ~~~python
                builder.list_one()
            ~~~
        """
        self.method = 'list_one'
        return self

    @set_method_call
    def download(self) -> 'FileConnectorBuilder':
        """
        Configures the builder to download a file from the specified organization.

        This method sets the internal state of the builder to prepare for a file download operation. It does not execute the operation immediately but prepares the necessary configurations for when the `execute` method is called.

        Returns:
            FileConnectorBuilder: Returns itself to allow for method chaining. 
        Example:
            ~~~python
                builder.download()
            ~~~
        """
        self.method = 'download'
        return self

    @set_method_call
    def delete(self)  -> 'FileConnectorBuilder':
        self.method = 'delete'
        return self

    @set_method_call
    def build(self) -> 'FileConnectorBuilder':
        if self.method_calls.count('build') > 1:
            raise RuntimeError("build() already build")
        if 'build_execute' in self.method_calls:
            raise Exception("You cannot use 'build()' together with 'build_execute()'")
        self._validate_builds()
        return self

    @set_method_call
    def build_execute(self):
        if 'build' in self.method_calls:
            raise RuntimeError("You cannot use 'build_execute()' together with 'build()'")
        if 'execute' in self.method_calls:
            raise RuntimeError("You cannot use 'build_execute()' together with 'execute()'")
        self._validate_builds()
        return self.execute()

    @set_method_call
    def execute(self) -> Response:
        if 'build' in self.method_calls:
            if self.method_calls[-2] != 'build':
                raise RuntimeError("The build() function must be the last method invoked before execute.")
        if 'build' not in self.method_calls and 'build_execute' not in self.method_calls:
            raise RuntimeError("You need to use a build() or build_execute() before execute().")

        self.url = f'{self.base_url}/fileConnector/organizations/{self.organization_name}'

        methods = {
            'upload': self._execute_upload,
            'list_all': self._execute_list,
            'list_one': self._execute_list_one,
            'download': self._execute_download,
            'delete': self._execute_delete
        }
        if self.method in {'list_all', 'list_one'} and self.format_data is None:
            self.format_data = "dict"

        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _classify_upload_response(self, response):
        """
        Aplica la semántica del OpenAPI para /upload:
          - 204: success
          - 200: partial success (devuelve errorList en JSON)
        Otros códigos se dejan como error devolviendo el payload del backend si existe.
        """
        content_type = (response.headers.get("Content-Type") or "").lower()
        has_body = bool(getattr(response, "content", b""))
        payload = None
        if has_body and "application/json" in content_type:
            try:
                payload = response.json()
            except ValueError:
                payload = None

        if response.status_code == 204:
            return {
                "result": "success"
            }
        elif response.status_code == 200:
            errors = None
            if isinstance(payload, dict):
                errors = payload.get("errors")
            return {
                "result": "partial_success",
                "message": "Partial upload: some files were not uploaded",
                "errors": errors,
                "data": payload
            }
        else:
            if payload is not None:
                return {"error": payload}
            try:
                return {"error": parse_json(response.text)}
            except Exception:
                return {"error": response.text}

    def _execute_upload(self) -> dict:
        url = f"{self.url}/upload"
        results = []

        if self.df is not None:
            for _, row in self.df.iterrows():
                file_path = str(row.get("local_file", "")).strip()
                if not file_path:
                    results.append({"status_code": 400, "error": "Missing 'local_file' in row"})
                    continue
                if not os.path.isfile(file_path):
                    results.append({"status_code": 400, "file": file_path, "error": "Local file not found"})
                    continue

                destiny_path = row.get("destiny_path", None)
                if destiny_path is None or (isinstance(destiny_path, float) and pd.isna(destiny_path)):
                    df_def = (self.df_defaults or {})
                    destiny_path = df_def.get("destiny_path", df_def.get("path", None))
                    if destiny_path is None:
                        destiny_path = self.path if self.path is not None else "/"
                destiny_path = str(destiny_path)
                if destiny_path and not destiny_path.endswith("/"):
                    destiny_path += "/"

                if "overwrite" in row and pd.notna(row["overwrite"]):
                    overwrite = bool(row["overwrite"])
                elif (self.df_defaults or {}).get("overwrite") is not None:
                    overwrite = bool(self.df_defaults["overwrite"])
                elif self.overwrite_files is not None:
                    overwrite = bool(self.overwrite_files)
                else:
                    overwrite = False

                meta = {"destinyPath": destiny_path, "overwriteFiles": overwrite}
                data = {"meta": json.dumps(meta)}

                lf = file_path.lower()
                if lf.endswith((".tar.gz", ".tgz")):
                    ct = "application/gzip"
                elif lf.endswith((".tar.bz2", ".tbz2")):
                    ct = "application/x-bzip2"
                elif lf.endswith(".tar"):
                    ct = "application/x-tar"
                elif lf.endswith(".zip"):
                    ct = "application/zip"
                else:
                    ct = "application/octet-stream"

                try:
                    with open(file_path, "rb") as fh:
                        multipart = {"file": (os.path.basename(file_path), fh, ct)}
                        response = send_request(
                            method="post",
                            headers=self.client.headers,
                            data=data,
                            url=url,
                            files=multipart
                        )
                    res = {
                        "file": file_path,
                        "destinyPath": destiny_path,
                        "status_code": response.status_code
                    }
                    classified = self._classify_upload_response(response)
                    res.update(classified)
                    results.append(res)
                except Exception as e:
                    results.append({
                        "file": file_path,
                        "destinyPath": destiny_path,
                        "overwrite": overwrite,
                        "status_code": 500,
                        "error": f"Local error opening file: {e}"
                    })
            return {"results": results}

        paths = self.local_file.get("paths_files", [])
        for file_path in paths:
            meta = {
                "destinyPath": self.path,
                "overwriteFiles": bool(self.overwrite_files) if self.overwrite_files is not None else False
            }
            data = {"meta": json.dumps(meta)}

            lf = file_path.lower()
            if lf.endswith((".tar.gz", ".tgz")): ct = "application/gzip"
            elif lf.endswith((".tar.bz2", ".tbz2")): ct = "application/x-bzip2"
            elif lf.endswith(".tar"): ct = "application/x-tar"
            elif lf.endswith(".zip"): ct = "application/zip"
            else: ct = "application/octet-stream"

            try:
                with open(file_path, "rb") as fh:
                    multipart = {"file": (os.path.basename(file_path), fh, ct)}
                    response = send_request(
                        method="post", headers=self.client.headers, data=data, url=url, files=multipart
                    )
            except Exception as e:
                results.append({"file": file_path, "status_code": 500, "error": f"Local error opening file: {e}"})
                continue

            res = {"file": file_path, "status_code": response.status_code}
            classified = self._classify_upload_response(response)
            res.update(classified)
            results.append(res)

        return {"results": results}

    def _execute_list(self) -> Response:
        url = f"{self.url}/list"
        response = send_request(method='get', headers=self.client.headers, url=url, params={'path': self.path})
        result = {'status_code': response.status_code}
        if response.status_code == 200:
            data = parse_json(response.text)
            if self.format_data == "pandas":
                return pd.DataFrame(data)
            result['data'] = data
        else:
            result['error'] = response.text
        return result

    def _execute_list_one(self) -> Response:
        url = f"{self.url}/list"
        response = send_request(method='get', headers=self.client.headers, url=url, params={'path': self.path})
        result = {'status_code': response.status_code}
        if response.status_code == 200:
            data = parse_json(response.text)
            found = next((item for item in data if item.get("name") == self.find_file_name), None)
            if not found:
                raise ValueError(f"File name: {self.find_file_name} not found in path: {self.path}")
            if self.format_data == "pandas":
                return pd.DataFrame([found])
            result['data'] = found
        else:
            result['error'] = response.text
        return result

    def _execute_download(self) -> Response:
        url = f"{self.url}/download"
        results = []

        def _resolve_dest_dir(out_dir: str | None) -> str:
            dest = out_dir if out_dir else (self.output_path or os.getcwd())
            dest = dest if os.path.isabs(dest) else os.path.abspath(dest)
            os.makedirs(dest, exist_ok=True)
            return dest

        if self.df is not None:
            for _, row in self.df.iterrows():
                rpath = row.get("path", None)
                if rpath is None or (isinstance(rpath, float) and pd.isna(rpath)):
                    rpath = (self.df_defaults or {}).get("path", None)
                    if rpath is None:
                        rpath = self.path
                if not rpath:
                    results.append({"status_code": 400, "error": "Missing 'path' in row"})
                    continue
                rpath = str(rpath)
                if rpath and not rpath.endswith("/"):
                    rpath += "/"

                fname = row.get("filename", None)
                if not fname or (isinstance(fname, float) and pd.isna(fname)):
                    results.append({"status_code": 400, "path": rpath, "error": "Missing 'filename' in row"})
                    continue
                fname = str(fname)

                out_dir = row.get("output_path", None)
                if out_dir is None or (isinstance(out_dir, float) and pd.isna(out_dir)):
                    out_dir = (self.df_defaults or {}).get("output_path", None)
                    if out_dir is None:
                        out_dir = self.output_path

                dest_dir = _resolve_dest_dir(out_dir)
                dest_path = os.path.join(dest_dir, os.path.basename(fname) or "downloaded_file")
                remote_path = f"{rpath}{fname}"

                try:
                    response = send_request(
                        method='get', headers=self.client.headers, url=url,
                        params={'path': remote_path}, stream=True
                    )
                    if response.status_code == 200:
                        with open(dest_path, "wb") as f:
                            for chunk in getattr(response, "iter_content", lambda **k: [])(chunk_size=8192):
                                if chunk: f.write(chunk)
                        results.append({"status_code": 200, "path": rpath, "file": fname, "output_path": dest_path})
                    else:
                        try:
                            error_json = parse_json(response.text)
                            message = error_json.get("errors", [{}])[0].get("message", response.text)
                        except Exception:
                            message = response.text
                        results.append({"status_code": response.status_code, "path": rpath, "file": fname, "error": message})
                except Exception as e:
                    results.append({"status_code": 500, "path": rpath, "file": fname, "error": f"Local error: {e}"})
            return {"results": results}

        if not self.filename["files"]:
            raise ValueError("No files provided. Use add_remote_file()/add_remote_multiple_files() or from_dataframe().")

        dest_dir = _resolve_dest_dir(self.output_path)
        for filename in self.filename["files"]:
            local_name = os.path.basename(filename) or "downloaded_file"
            remote_path = f"{self.path}{filename}"
            dest_path = os.path.join(dest_dir, local_name)

            try:
                response = send_request(
                    method='get', headers=self.client.headers, url=url, params={'path': remote_path}, stream=True
                )
                if response.status_code == 200:
                    with open(dest_path, "wb") as f:
                        for chunk in getattr(response, "iter_content", lambda **k: [])(chunk_size=8192):
                            if chunk: f.write(chunk)
                    results.append({"status_code": 200, "file": filename, "output_path": dest_path})
                else:
                    try:
                        error_json = parse_json(response.text)
                        message = error_json.get("errors", [{}])[0].get("message", response.text)
                    except Exception:
                        message = response.text
                    results.append({"status_code": response.status_code, "file": filename, "error": message})
            except Exception as e:
                results.append({"status_code": 500, "file": filename, "error": f"Local error: {e}"})

        return {"results": results}

    def _execute_delete(self) -> Response:
        url = f"{self.url}/delete"

        def _norm_path(p: str | None) -> str:
            if p is None: return ""
            p = str(p).rstrip("/")
            return "" if p == "/" else p

        if self.df is not None:
            results = []
            for _, row in self.df.iterrows():
                destiny_path = row.get("path", None)
                if destiny_path is None or (isinstance(destiny_path, float) and pd.isna(destiny_path)):
                    destiny_path = (self.df_defaults or {}).get("path", None)
                    if destiny_path is None:
                        destiny_path = self.path
                destiny_path = _norm_path(destiny_path)

                filename = row.get("filename", None)
                if filename is None or (isinstance(filename, float) and pd.isna(filename)) or str(filename) == "":
                    file_name = ""  
                else:
                    file_name = str(filename)

                payload = {"destinyPath": destiny_path, "fileName": file_name}
                try:
                    response = send_request(method="post", url=url, headers=self.client.headers, json_payload=payload)
                    if response.status_code == 204:
                        results.append({"status_code": 204, "path": destiny_path})
                    else:
                        try:
                            err = parse_json(response.text)
                            msg = err.get("errors", [{}])[0].get("message", response.text)
                        except Exception:
                            msg = response.text
                        results.append({"status_code": response.status_code, "path": destiny_path, "error": msg})
                except Exception as e:
                    results.append({"status_code": 500, "path": destiny_path, "error": f"Local error: {e}"})
            return {"results": results}

        destiny_path = _norm_path(self.path)

        if self.filename["files"]:
            results = []
            for fname in self.filename["files"]:
                payload = {"destinyPath": destiny_path, "fileName": fname}
                try:
                    response = send_request(method="post", url=url, headers=self.client.headers, json_payload=payload)
                    if response.status_code == 204:
                        results.append({"status_code": 204, "path": destiny_path, "file": fname})
                    else:
                        try:
                            err = parse_json(response.text)
                            msg = err.get("errors", [{}])[0].get("message", response.text)
                        except Exception:
                            msg = response.text
                        results.append({"status_code": response.status_code, "path": destiny_path, "file": fname, "error": msg})
                except Exception as e:
                    results.append({"status_code": 500, "path": destiny_path, "file": fname, "error": f"Local error: {e}"})
            return {"results": results}

        payload = {"destinyPath": destiny_path, "fileName": ""}
        try:
            response = send_request(method="post", url=url, headers=self.client.headers, json_payload=payload)
        except Exception as e:
            return {"status_code": 500, "error": f"Local error: {e}", "path": destiny_path}

        result = {"status_code": response.status_code, "path": destiny_path}
        if response.status_code != 204:
            try:
                err = parse_json(response.text)
                msg = err.get("errors", [{}])[0].get("message", response.text)
            except Exception:
                msg = response.text
            result["error"] = msg
        return result
        

    def _validate_builds(self):
        if not self.organization_name:
            raise ValueError("with_organization_name() is required")

        if self.df is not None:
            if self.method == "upload":
                if "local_file" not in self.df.columns:
                    raise ValueError("Uploading with from_dataframe requires 'local_file' column")
                return self

            if self.method == "download":
                mix = any([
                    self.path is not None,
                    bool(self.filename["files"]),
                    self.output_path is not None
                ])
                if mix:
                    missing = []
                    if self.path is None: missing.append("with_destiny_path()")
                    if not self.filename["files"]: missing.append("add_remote_file() / add_remote_multiple_files()")
                    if self.output_path is None: missing.append("with_output_path()")
                    if missing:
                        raise ValueError(
                            "If you mix `from_dataframe` with setters for download, you must use all of them:"
                            + ", ".join(missing)
                            + ". O usa solo from_dataframe."
                        )
                if "path" not in self.df.columns and not (self.df_defaults or {}).get("path") and self.path is None:
                    raise ValueError("download with from_dataframe requires column 'path' or default 'path' or with_destiny_path()")
                if "filename" not in self.df.columns:
                    raise ValueError("download con from_dataframe requiere columna 'filename'")
                return self

            if self.method == "delete":
                if "path" not in self.df.columns and not (self.df_defaults or {}).get("path") and self.path is None:
                    raise ValueError("delete with from_dataframe requires column 'path' or default 'path' or with_destiny_path()")
                return self

        spec = {
            'list_all': {
                'required':  ['organization_name', 'path'],
                'forbidden': ['find_file_name', 'filename', 'output_path', 'local_file'],
                'choices':   {'format_data': ('dict', 'pandas')},
            },
            'list_one': {
                'required':  ['organization_name', 'path', 'find_file_name'],
                'forbidden': ['filename', 'output_path', 'local_file'],
                'choices':   {'format_data': ('dict', 'pandas')},
            },
            'download': {
                'required':  ['organization_name', 'path', 'filename', 'output_path'],
                'forbidden': ['find_file_name', 'local_file', 'format_data'],
            },
            'upload': {
                'required':  ['organization_name','local_file'],
                'forbidden': ['find_file_name', 'filename', 'output_path'],
            },
            'delete': {
                'required':  ['organization_name', 'path'],
                'forbidden': ['find_file_name', 'format_data', 'local_file'],
            },
        }

        state = {
            'organization_name': self.organization_name,
            'path': self.path,
            'find_file_name': getattr(self, 'find_file_name', None),
            'format_data': self.format_data,
            'filename': self.filename if self.filename["files"] else None,
            'output_path': self.output_path,
            'local_file': self.local_file if self.local_file["paths_files"] else None,
        }

        allowed_method_calls = {'list_all', 'list_one', 'download', 'upload', 'delete'}

        field_aliases = {
            'organization_name': 'with_organization_name',
            'path':              'with_destiny_path',
            'find_file_name':    'with_find_name',
            'format_data':       'with_format',
            'filename':          'add_remote_file / add_remote_multiple_files',
            'output_path':       'with_output_path',
            'local_file':        'add_local_file / add_local_multiple_files',
        }

        method_aliases = {
            'list_all': 'list_all()',
            'list_one': 'list_one()',
            'download': 'download()',
            'upload': 'upload()',
            'delete': 'delete()'
        }

        validate_build(
            method=self.method,
            state=state,
            spec=spec,
            used_methods=self.method_calls,
            allowed_method_calls=allowed_method_calls,
            field_aliases=field_aliases,
            method_aliases=method_aliases,
        )
        return self
