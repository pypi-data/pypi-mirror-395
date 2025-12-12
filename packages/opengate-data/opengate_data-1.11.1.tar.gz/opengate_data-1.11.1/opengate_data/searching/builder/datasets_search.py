"""  DatasetsSearchBuilder """

import requests
import pandas as pd
from typing import Any
from io import StringIO
from opengate_data.searching.search import SearchBuilder
from opengate_data.utils.utils import send_request, handle_error_response, handle_exception, set_method_call, \
    validate_type


class DatasetsSearchBuilder(SearchBuilder):
    """ Dataset Search Builder """

    def __init__(self, opengate_client):
        super().__init__()
        self.client = opengate_client
        self.headers = self.client.headers
        self.organization_name: str | None = None
        self.identifier: str | None = None
        self.body_data: dict[str, Any] = {}
        self.format_data: str = 'dict'
        self.utc: bool = False
        self.method_calls: list = []

    @set_method_call
    def with_organization_name(self, organization_name: str) -> 'DatasetsSearchBuilder':
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
    def with_identifier(self, identifier: str) -> 'DatasetsSearchBuilder':
        """
        Set identifier

        Returns:
            DatasetsSearchBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_identifier("identifier")
            ~~~
        """
        validate_type(identifier, str, "Identifier")
        self.identifier = identifier
        return self

    def with_utc(self) -> 'DatasetsSearchBuilder':
        """
        Set UTC

        Returns:
            DatasetsSearchBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_utc()
            ~~~
        """
        self.utc = True
        return self

    @set_method_call
    def with_format(self, format_data: str) -> 'DatasetsSearchBuilder':
        """
        Formats the flat entities data based on the specified format ('csv', 'dict', or 'pandas').

        Args:
            format_data (str): The format to use for the data.

        Returns:
            DatasetsSearchBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_format("dict")
                builder.with_format("pandas")
                builder.with_format("csv")
            ~~~
        """
        validate_type(format_data, str, "Format data")
        self.format_data = format_data
        if self.format_data == 'csv' or self.format_data == 'pandas':
            self.headers['Accept'] = 'text/plain'
        else:
            self.headers['Accept'] = 'application/json'
        return self

    @set_method_call
    def build(self) -> 'DatasetsSearchBuilder':
        """
        Finalizes the construction of the operation search configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

        Returns:
            DatasetsSearchBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.

        Note:
            This method should be used as a final step before `execute` to prepare the operations search configuration. It does not modify the state but ensures that the builder's state is ready for execution.

        Example:
            ~~~python
                builder.build()
            ~~~
        """
        self._validate_builds()

        if 'build_execute' in self.method_calls:
            raise Exception(
                "You cannot use build() together with build_execute()")

        return self

    @set_method_call
    def build_execute(self):
        """
        Executes the data sets search immediately after building the configuration.

        This method is a shortcut that combines building and executing in a single step.

        Returns:
            dict: A dictionary containing the execution response which includes the status code and potentially other metadata about the execution.

        Raises:
            ValueError: If `build` has already been called on this builder instance.

        Example:
            ~~~python
                new_data_sets_search_builder.with_format("csv").with_organization_name(organization).build_execute()
                new_data_sets_search_builder.with_filter(filter).with_organization_name(organization).with_format("pandas").build_execute()
                new_data_sets_search_builder.with_filter(filter).with_organization_name(organization).with_format("dict").build_execute()
            ~~~
        """
        if 'build' in self.method_calls:
            raise ValueError(
                "You cannot use build_execute() together with build()")

        if 'execute' in self.method_calls:
            raise ValueError(
                "You cannot use build_execute() together with execute()")

        self._validate_builds()
        return self.execute()

    def _validate_builds(self):
        if self.method_calls.count('with_format') > 1:
            raise Exception(
                "You cannot use more than one 'with_format()' method")

        if "with_organization_name" not in self.method_calls or "with_identifier" not in self.method_calls:
            raise Exception(
                "It is mandatory to use 'with_organization_name()' and 'with_identifier()' methods")

        select = self.body_data.get("select")
        if select is not None:
            if not all(isinstance(item, str) for item in select):
                raise ValueError(
                    "Data sets only supports simple select (list of strings)")

        return self

    @set_method_call
    def execute(self):
        """
        Executes the data set search based on the built configuration.

        Returns:
            dict, csv or dataframe: The response data in the specified format.

        Raises:
            Exception: If the build() method was not called before execute().

        Example:
            ~~~python
                new_data_sets_search_builder.with_format("csv").with_organization_name(organization).build().execute()
                new_data_sets_search_builder.with_filter(filter).with_organization_name(organization).with_format("pandas").build().execute()
                new_data_sets_search_builder.with_filter(filter).with_organization_name(organization).with_format("dict").build().execute()
            ~~~
        """
        if 'build' in self.method_calls:
            if self.method_calls[-2] != 'build':
                raise Exception(
                    "The 'build()' function must be the last method invoked before execute."
                )

        if 'build' not in self.method_calls and 'build_execute' not in self.method_calls:
            raise Exception(
                "You need to use a 'build()' or 'build_execute()' function the last method invoked before execute"
            )

        if self.client.url is None:
            base_url = 'https://collections:8544'
        else:
            base_url = f'{self.client.url}/north'

        url = f'{base_url}/v80/datasets/provision/organizations/{self.organization_name}/{self.identifier}/data?utc={self.utc}'

        if self.format_data == 'csv':
            return self._csv_request(url)

        if self.format_data == 'pandas':
            return self._csv_pandas_request(url)

        return self._dict_pandas_request(url)

    def _get_dataset_definition(self) -> dict[str, Any]:
        if self.client.url is None:
            base_url = 'https://collections:8544'
        else:
            base_url = f'{self.client.url}/north'

        url = f'{base_url}/v80/datasets/provision/organizations/{self.organization_name}/{self.identifier}'

        headers = self.client.headers.copy()
        headers["Accept"] = "application/json"

        response = send_request(
            method="get",
            url=url,
            headers=headers,
        )

        if response.status_code != 200:
            return handle_error_response(response)

        return response.json()

    def _build_type_map(self, definition: dict[str, Any]) -> dict[str, str]:
        type_map: dict[str, str] = {}

        for col in definition.get("columns", []):
            name = col.get("name")
            col_type = col.get("type")
            if name and col_type:
                type_map[name] = col_type

        for ctx in definition.get("context", []):
            name = ctx.get("name")
            col_type = ctx.get("type")
            if name and col_type and name not in type_map:
                type_map[name] = col_type

        return type_map

    def _build_converters_from_type_map(self, type_map: dict[str, str]):
        def make_numeric_converter(kind: str):
            def conv(x: str):
                if x is None or x == "":
                    return None
                try:
                    v = float(x)
                except ValueError:
                    return None
                if kind == "integer":
                    try:
                        return int(v)
                    except (TypeError, ValueError):
                        return None
                return v
            return conv

        def datetime_converter_factory(utc: bool):
            def conv(x: str):
                if x is None or x == "":
                    return pd.NaT
                return pd.to_datetime(x, errors="coerce", utc=utc)
            return conv

        def bool_converter(x: str):
            if x is None or x == "":
                return None
            return str(x).strip().lower() in (
                "true",
                "1",
                "t",
                "yes",
                "y",
                "si",
                "sí",
            )

        def string_converter(x: str):
            if x is None or x == "":
                return None
            return str(x)

        converters: dict[str, Any] = {}

        for name, t in type_map.items():
            t_low = str(t).lower()

            if t_low in ("number", "integer", "float", "double"):
                converters[name] = make_numeric_converter(t_low)

            elif t_low in ("date-time", "datetime", "date"):
                converters[name] = datetime_converter_factory(self.utc)

            elif t_low in ("boolean", "bool"):
                converters[name] = bool_converter

            elif t_low in ("string", "text"):
                converters[name] = string_converter

        return converters

    def _csv_request(self, url: str):
        try:
            response = send_request(
                method="post", url=url, headers=self.client.headers, json_payload=self.body_data)
            if response.status_code != 200:
                return handle_error_response(response)
            return response.text

        except Exception as e:
            return handle_exception(e)
        
    def _csv_pandas_request(self, url: str) -> pd.DataFrame:

        try:
            response = send_request(
                method="post",
                url=url,
                headers=self.client.headers,
                json_payload=self.body_data
            )

            if response.status_code != 200:
                return handle_error_response(response)

            csv_text = response.text

            definition = self._get_dataset_definition()

            if not isinstance(definition, dict):
                return definition

            type_map = self._build_type_map(definition)

            converters = self._build_converters_from_type_map(type_map)

            df = pd.read_csv(StringIO(csv_text), sep=';', converters=converters)

            df.attrs["og_types"] = type_map

            return df

        except Exception as e:
            return handle_exception(e)

    def _dict_pandas_request(self, url: str) -> Any:
        data = None
        all_results = []
        limit = self.body_data.get("limit", {})
        start = limit.get("start", 1)
        size = limit.get("size", 1000)
        has_limit = "limit" in self.body_data

        while True:
            self.body_data.setdefault("limit", {}).update(
                {"start": start, "size": size})
            try:
                response = requests.post(url, headers=self.client.headers, json=self.body_data, verify=False,
                                         timeout=3000)

                if response.status_code == 204:
                    if all_results:
                        break
                    return {'status_code': response.status_code}

                if response.status_code != 200 and response.status_code != 204:
                    return handle_error_response(response)

                data = response.json()

                if not data.get('data'):
                    break

                all_results.extend(data['data'])

                if has_limit:
                    break

                start += 1

            except Exception as e:
                return handle_exception(e)

        return self._format_results(all_results, data['columns'])

    def _format_results(self, all_results, columns):
        if self.format_data == 'dict':
            return {"columns": columns, "data": all_results}
        if self.format_data == 'pandas':
            return pd.DataFrame(all_results, columns=columns)
        raise ValueError(f"Unsupported format: {self.format_data}")
