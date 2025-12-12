"""Provision Timeseries Builder"""

from __future__ import annotations

from typing import Any

from requests import Response

from opengate_data.searching.search import SearchBuilder
from opengate_data.utils.utils import (
    send_request,
    set_method_call,
    parse_json,
    validate_type,
    validate_build_method_calls_execute,
    validate_build,
)

class TimeseriesBuilder(SearchBuilder):
    """ Class timeseries builder """
    def __init__(self, opengate_client):
        super().__init__()
        self.client = opengate_client
        if self.client.url is None:
            self.base_url = "https://frontend:8443/v80/provision/organization"
        else:
            self.base_url = f"{self.client.url}/north"

        self.organization_name: str | None = None
        self.identifier: str | None = None
        self.callback_url: str | None = None
        self.method: str | None = None 
        self.method_calls: list = []

    @set_method_call
    def with_organization_name(self, organization_name: str) -> "TimeseriesBuilder":
        """
        Specify the organization name.

        Args:
            organization_name (str): The name of the organization.

        Returns:
            TimeseriesBuilder: Returns self for chaining.

        Example:
            ~~~python
                builder.with_organization_name('organization_name')
            ~~~
        """
        validate_type(organization_name, str, "organization_name")
        self.organization_name = organization_name
        return self

    @set_method_call
    def with_identifier(self, identifier: str) -> "TimeseriesBuilder":
        """
         Specify the identifier for the pipeline.

         Args:
             identifier (str): The identifier for the pipeline.

         Returns:
             TimeseriesBuilder: Returns self for chaining.

        Example:
            ~~~python
                builder.with_identifier('identifier')
            ~~~
         """
        validate_type(identifier, str, "identifier")
        self.identifier = identifier
        return self

    @set_method_call
    def with_callback(self, callback_url: str) -> "TimeseriesBuilder":
        """
        Specify the callback URL to be triggered once the export operation completes.

        This value will be added to the HTTP headers under the key `callback` when the
        export request is sent. The backend will later invoke this URL to notify the
        client once the export process is finished (or failed), if supported.

        Args:
            callback_url (str): A valid URL that will be called by the backend as a callback.

        Returns:
            TimeseriesBuilder: Returns the instance itself to allow fluent chaining.

        Example:
            ~~~python
            builder.with_callback("callback")
            ~~~
        """
        validate_type(callback_url, str, "callback")
        self.callback_url = callback_url
        return self

    @set_method_call
    def with_output_file(
        self,
        filename: str,
        content_type: str | None = None,
    ) -> "TimeseriesBuilder":
        """
        Defines the exported Parquet file that will be generated in the backend.

        This sets the following JSON structure inside the export request body::

            {
                "outputFile": {
                    "name": "<filename>",
                    "contentType": "application/vnd.apache.parquet"
                }
            }

        By default, `contentType` is always set to
        ``application/vnd.apache.parquet`` as required by the API
        specification. The parameter is optional and mainly kept for
        forward-compatibility.

        Args:
            filename (str): The desired Parquet filename (e.g., "timeserie.parquet").
            content_type (str | None): Content type of the file. If not provided,
                it defaults to "application/vnd.apache.parquet".

        Returns:
            TimeseriesBuilder: Returns the current instance to allow method chaining.
        """
        validate_type(filename, str, "outputFile.name")
        if content_type is None:
            content_type = "application/vnd.apache.parquet"
        else:
            validate_type(content_type, str, "outputFile.contentType")

        self.body_data.setdefault("outputFile", {})
        self.body_data["outputFile"]["name"] = filename
        self.body_data["outputFile"]["contentType"] = content_type
        return self



    @set_method_call
    def export(self) -> "TimeseriesBuilder":
        """
        Configure the builder to request the export of a timeseries to a Parquet file.

        The backend will start an asynchronous export process.  
        Depending on the state of the timeseries, the response may be:

            - 202: Export request accepted (export is being generated in background)
            - 204: The timeseries exists but has no data to export
            - 409: The timeseries is already being exported by another process
            - 400: Bad request (invalid JSON, filter, select, etc.)

        The export configuration can include:
            - filter
            - select
            - limit
            - outputFile.name (via with_output_file)
            - callback (via with_callback → added as header)

        Returns:
            TimeseriesBuilder: The same builder instance to allow fluent chaining.

        Example:
            ~~~python
            builder \
                .with_organization_name("organization") \
                .with_identifier("identifier") \
                .with_output_file("file.parquet") \
                .export() \
            ~~~
        """
        self.method = "export"
        return self


    @set_method_call
    def export_status(self) -> "TimeseriesBuilder":
        """
        Configure the builder to retrieve the current export status of a timeseries.

        If a callback URL was defined with `with_callback()`,
        it will be included in the request headers.

        Returns:
            TimeseriesBuilder: The current instance for method chaining.

        Example:
            ~~~python
            builder \
                .with_organization_name("organization") \
                .with_identifier("identifier") \
                .export_status() \
            ~~~
        """
        self.method = "status"
        return self

    @set_method_call
    def build(self) -> "TimeseriesBuilder":
        """
        Finalizes the construction of the asset configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

        Returns:
            ProvisionAssetBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.

        Example:
            ~~~python
                builder.build()
            ~~~
        """
        self._validate_builds()
        return self

    @set_method_call
    def build_execute(self):
        """
        Executes the timeseries search immediately after building the configuration.

        This method is a shortcut that combines building and executing in a single step.

        Returns:
            dict: A dictionary containing the execution response which includes the status code and potentially other metadata about the execution.

        Raises:
            ValueError: If `build` has already been called on this builder instance.

        Example:
            ~~~python
                builder.build_execute()
            ~~~
        """
        if 'build' in self.method_calls:
            raise ValueError(
                "You cannot use 'build_execute()' together with 'build()'")

        if 'execute' in self.method_calls:
            raise ValueError(
                "You cannot use 'build_execute()' together with 'execute()'")
        
        self._validate_builds()

        return self.execute()

    @set_method_call
    def execute(self) -> Any:
        """
        Execute the configured asset and return the response.

        This method executes the operation that has been configured using the builder pattern. It ensures that the `build` method has been called and that it is the last method invoked before `execute`. Depending on the configured method (e.g., create, find, update, delete), it calls the appropriate internal execution method.

        Returns:
            requests.Response: The response object from the executed request.

        Raises:
            Exception: If the `build` method has not been called or if it is not the last method invoked before `execute`.
            ValueError: If the configured method is unsupported.

        Example:
            ~~~python
                builder.execute()
            ~~~
        """
        validate_build_method_calls_execute(self.method_calls)

        url = f"{self.base_url}/v80/timeseries/provision/organizations/{self.organization_name}/{self.identifier}/export"

        methods = {
            "export": self._execute_export,
            "status": self._execute_status,
        }

        func = methods.get(self.method)
        if func is None:
            raise ValueError(f"Unsupported method: {self.method!r}")

        return func(url)
    
    def _build_headers(self) -> dict[str, str]:
        headers = dict(self.client.headers or {})
        if self.callback_url:
            headers["callback"] = self.callback_url
        return headers
    
    def _execute_export(self, url: str) -> dict[str, Any]:
        body = self.body_data or {}
        headers = self._build_headers()

        response = send_request(
            method="post",
            headers=headers,
            url=url,
            json_payload=body,
        )
        
        result = {"status_code": response.status_code}

        if response.status_code == 202:
            result['data'] =  "Export request has been accepted and it's currently being exported in the background."
        
        elif response.status_code == 204:
            result['data'] = "The selected timeseries has no data"

        elif response.status_code == 409:
            result['data'] = "This timeseries is currently being exported by another process"
        else:
            if response.text:
                result['error'] = response.text
        return result

    def _execute_status(self, url: str) -> dict[str, Any]:
        import time

        headers = self._build_headers()
        headers["Accept"] = "application/json"

        max_attempts = 10
        delay_seconds = 2

        response = None
        for attempt in range(max_attempts):
            response = send_request(
                method="get",
                headers=headers,
                url=url,
            )

            if response.status_code != 406:
                break

            time.sleep(delay_seconds)

        result = {"status_code": response.status_code}

        if response.status_code == 200:
            result["data"] = parse_json(response.text)
        else:
            if response.text:
                result["error"] = response.text

        return result




    def _validate_builds(self):
        state = {
            "organization_name": self.organization_name,
            "identifier": self.identifier,
            "callback_url": self.callback_url,
            "body_data": self.body_data if self.body_data else None,
        }

        spec = {
            "export": {
                "required": ["organization_name", "identifier"],
                "forbidden": [],
            },
            "status": {
                "required": ["organization_name", "identifier"],
                "forbidden": ["body_data"],
            },
        }

        allowed_method_calls = {"export", "export_status"}

        field_aliases = {
            "organization_name": "with_organization_name",
            "identifier": "with_identifier",
            "callback_url": "with_callback",
            "body_data": "with_filter / with_select / with_limit / with_output_file",
        }

        method_aliases = {
            "export": "export()",
            "status": "export_status()",
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

