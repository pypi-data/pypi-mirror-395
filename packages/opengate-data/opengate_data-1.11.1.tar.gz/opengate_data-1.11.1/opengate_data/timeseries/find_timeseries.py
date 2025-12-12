from opengate_data.searching.search import SearchBuilder
from requests import Response
from opengate_data.utils.utils import send_request, set_method_call, parse_json, validate_type, handle_exception, handle_error_response
import os
import pandas as pd


class FindTimeseriesBuilder(SearchBuilder):
    """ Find time series Builder """

    def __init__(self, opengate_client):
        self.client = opengate_client
        if self.client.url is None:
            self.base_url = 'https://collections:8544'
        else:
            self.base_url = f'{self.client.url}/north'
        self.method_calls: list = []
        self.method: str | None = None
        self.identifier: str | None = None
        self.find_name: str | None = None
        self.data_env: str | None = None
        self.context: str | None = None
        self.datastreams: str | None = None
        self.organization_name: str | None = None
        self.config_file: str | None = None
        self.section: str | None = None
        self.config_key: str | None = None
        self.format_data: str = 'dict'
        self.env_key: str | None = None
        self.env_prefer: str = "auto"          
        self.config_value: str | None = None
        self.config_prefer: str = "auto"

    @set_method_call
    def with_expand(self, expand: str) -> 'FindTimeseriesBuilder':
        """
        With expand, select the data field to show information, columns, context or columns.context.

        Args:
            expand (str):

        Returns:
            FindTimeseriesBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                # expand=columns, expand=context, expand=columns.context
                builder.with_expand("columns")
            ~~~
        """
        if expand not in ["columns", "context", "both"]:
            raise ValueError("expand must be 'columns', 'context' or 'columns.context'")
        validate_type(expand, str, "Expand")
        self.context = expand
        return self
    
    @set_method_call
    def with_datastreams(self, datastreams: str) -> 'FindTimeseriesBuilder':
        """
        With dataStreams, select the dataStreams to filter the Timeseries. To be accept and intepreted by the System the dataStream will be in format URL.
        
        Args:
            datastreams (str):

        Returns:
            FindTimeseriesBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                # example: dataStreams=provision.device.identifier,provision.device.communicationModules.subscription.address
                builder.with_datastreams("provision.device.identifier")
            ~~~
        """
        validate_type(datastreams, str, "Expand")
        self.datastreams = datastreams

    @set_method_call
    def with_organization_name(self, organization_name: str) -> 'FindTimeseriesBuilder':
        """
        Set organization name

        Args:
            organization_name (str):

        Returns:
            timeseriesFindTimeseriesBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_organization_name("organization_name")
            ~~~
        """
        validate_type(organization_name, str, "Organization")
        self.organization_name = organization_name
        return self
    
    @set_method_call
    def with_format(self, format_data: str) -> 'FindTimeseriesBuilder':
        """
        Formats the flat entities data based on the specified format ('csv', 'dict', or 'pandas'). By default, the data is returned as a dictionary.

        Args:
            format_data (str): The format to use for the data.

        Example:
            builder.with_format('dict')
            builder.with_format('pandas')

        Returns:
            SearchBuilderBase: Returns itself to allow for method chaining.
        """
        validate_type(format_data, str, "Format data")
        self.format_data = format_data
        return self
    
    @set_method_call
    def with_identifier(self, identifier: str) -> 'FindTimeseriesBuilder':
        """
        set the timeseries identifier.

        Args:
            identifier (str): The identifier of the timeseries.

        Returns:
            FindTimeseriesBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_identifier("timeseries_id")
            ~~~
        """
        validate_type(identifier, str, "Find identifier")
        self.identifier = identifier
        return self
    
    @set_method_call
    def with_config_file(self, config_file: str, section: str, config_key: str, prefer: str = "auto") -> 'FindTimeseriesBuilder':
        """
            Reads a value from the INI and saves it as a source. 'prefer' controls whether the value will be interpreted as identifier, name, or auto (first id, then name).
        """
        validate_type(config_file, str, "Config file")
        validate_type(section, str, "Section")
        validate_type(config_key, str, "Config Key")
        validate_type(prefer, str, "Prefer")
        if prefer not in {"auto", "identifier", "name"}:
            raise ValueError("prefer must be 'auto', 'identifier' or 'name'")

        config_file_path = os.path.abspath(config_file)
        self.config_file = config_file_path
        self.section = section
        self.config_key = config_key
        self.config_prefer = prefer

        import configparser
        config = configparser.ConfigParser()
        read_ok = config.read(config_file_path, encoding="utf-8-sig")
        if not read_ok:
            raise FileNotFoundError(f"No pude leer el archivo INI en {config_file_path}")
        if not config.has_section(section):
            raise configparser.NoSectionError(section)
        if not config.has_option(section, config_key):
            raise configparser.NoOptionError(config_key, section)

        self.config_value = config.get(section, config_key).strip()
        return self


    @set_method_call
    def with_name(self, find_name: str) -> 'FindTimeseriesBuilder':
        """
        Specify the name to find.

        Args:
            find_name (str): The name of the transformer.

        Returns:
            AITransformersBuilder: Returns self for chaining.

        Example:
            ~~~python
                builder.with_find_by_name('transformer_name')
            ~~~
        """
        validate_type(find_name, str, "Find name")
        self.find_name = find_name
        return self
    
    @set_method_call
    def with_env(self, env_key: str, prefer: str = "auto") -> 'FindTimeseriesBuilder':
        """
        Use an environment variable as the source. 'prefer' can be:
        - 'identifier' -> treat the value as an identifier
        - 'name' -> treat the value as a name
        - 'auto' -> try identifier and, if not, name
        """
        validate_type(env_key, str, "Env key")
        validate_type(prefer, str, "Prefer")
        if prefer not in {"auto", "identifier", "name"}:
            raise ValueError("prefer debe ser 'auto', 'identifier' o 'name'")
        self.env_key = env_key
        self.env_prefer = prefer
        return self


    @set_method_call
    def find_all(self) -> 'FindTimeseriesBuilder':
        """
        Searches for all available timeseries resources.

        Returns:
            FindTimeseriesBuilder: Returns the current instance to allow method chaining.

        Example:
            ~~~python
                builder.with_organization_name('my_organization').find_all()
            ~~~
        """
        self.method = 'find_all'
        return self

    @set_method_call
    def find_one(self) -> 'FindTimeseriesBuilder':
        """
        Searches for a single transformer resource by its identifier.

        This method prepares the request to find a specific transformer based on its identifier. The identifier is obtained automatically if not explicitly defined or can be obtained from a configuration file or environment variables.

        Returns:
            FindTimeseriesBuilder: Returns the current instance to allow method chaining.

        Example:
            ~~~python
                builder.with_organization_name('my_organization').with_organization_name("organization_name").with_format("dict").with_identifier("identifier").find_one().build().execute()
            ~~~
        """
        self.method = 'find_one'
        return self
    
    @set_method_call
    def build(self) -> 'FindTimeseriesBuilder':
        """
        Finalizes the construction of the IoT collection configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

        Returns:
            FindTimeseriesBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.

        Example:
            ~~~python
                builder.build()
            ~~~
        """

        if 'build_execute' in self.method_calls:
            raise Exception(
                "You cannot use 'build()' together with 'build_execute()'")
        
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
    def execute(self) -> Response:
        """
        Execute the configured operation and return the response.

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
        if 'build' in self.method_calls:
            if self.method_calls[-2] != 'build':
                raise Exception("The build() function must be the last method invoked before execute.")
        if 'build' not in self.method_calls and 'build_execute' not in self.method_calls:
            raise Exception("You need to use a build() or build_execute() function the last method invoked before execute.")

        self._validate_builds()

        base = f'{self.base_url}/v80/timeseries/provision/organizations/{self.organization_name}'

        from urllib.parse import urlencode, quote
        params = {}
        if self.context is not None:
            params["expand"] = self.context
        if self.datastreams is not None:
            params["dataStreams"] = self.datastreams

        self.url = base if not params else f"{base}?{urlencode(params, quote_via=quote)}"

        methods = {
            'find_all': self._execute_find_all,
            'find_one': self._execute_find_one,
        }
        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_find_all(self) -> str | dict[str, str | int]:
        result_get_data = self._get_data_response()
        return result_get_data

    def _execute_find_one(self) -> dict | pd.DataFrame:
        try:
            local_headers = {
                **self.client.headers,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            response = send_request(method='get', headers=local_headers, url=self.url)
            status_code = getattr(response, 'status_code')
            if status_code != 200:
                return handle_error_response(response)
            data = response.json()
        except Exception as e:
            return handle_exception(e)

        timeseries = data.get('timeseries', [])
        if not isinstance(timeseries, list):
            raise ValueError("Unexpected format: 'timeseries' is not a list.")

        by_id = {d.get("identifier"): d for d in timeseries if isinstance(d, dict)}
        by_name = {d.get("name"): d for d in timeseries if isinstance(d, dict)}

        def get_by_id(value: str) -> dict:
            ds = by_id.get(value)
            if not ds:
                raise ValueError(f"Timeserie with identifier '{value}' not found.")
            return ds

        def get_by_name(value: str) -> dict:
            ds = by_name.get(value)
            if not ds:
                raise ValueError(f"Timeserie with name '{value}' not found.")
            return ds

        def auto_lookup(value: str) -> dict:
            if value in by_id:
                return by_id[value]
            if value in by_name:
                return by_name[value]
            raise ValueError(f"Timeserie '{value}' not found by identifier or name.")

        if self.identifier:
            ds = get_by_id(self.identifier)
        elif self.find_name:
            ds = get_by_name(self.find_name)
        elif self.env_key:
            env_value = os.getenv(self.env_key)
            if not env_value:
                raise ValueError(f"La variable de entorno '{self.env_key}' no está definida.")
            match self.env_prefer:
                case "identifier":
                    ds = get_by_id(env_value)
                case "name":
                    ds = get_by_name(env_value)
                case "auto":
                    ds = auto_lookup(env_value)
                case _:
                    raise ValueError("Invalid env prefer.")
        elif self.config_value:
            match self.config_prefer:
                case "identifier":
                    ds = get_by_id(self.config_value)
                case "name":
                    ds = get_by_name(self.config_value)
                case "auto":
                    ds = auto_lookup(self.config_value)
                case _:
                    raise ValueError("Invalid config prefer.")
        else:
            raise ValueError("find_one() requires a source (with_identifier, with_name, with_env or with_config_file).")

        if self.format_data == "pandas":
            return pd.json_normalize([ds])
        return ds


    def _get_data_response(self) -> any:
        try:
            response = send_request(method='get', headers=self.client.headers, url=self.url)
            status_code = getattr(response, 'status_code')

            if status_code != 200:
                # Fallback defensivo por si algún proxy insiste con 406
                if status_code == 406:
                    response = send_request(method='get', headers={"Accept": "application/json"}, url=self.url)
                    status_code = getattr(response, 'status_code')
                    if status_code != 200:
                        return handle_error_response(response)
                else:
                    return handle_error_response(response)

            if self.format_data == 'dict':
                return response.json()

            if self.format_data == 'pandas':
                payload = response.json()
                items = payload.get('timeseries', payload.get('items', []))
                if isinstance(items, list):
                    return pd.json_normalize(items)
                if isinstance(items, dict):
                    return pd.json_normalize([items])
                # Si la API devuelve algo raro, devolvemos DF vacío antes que romper
                return pd.DataFrame()

            raise ValueError(f"Unsupported format: {self.format_data}. Use 'dict' or 'pandas'.")

        except Exception as e:
            return handle_exception(e)


    def _validate_builds(self):
        calls = tuple(self.method_calls)
        calls_set = set(calls)
        op = self.method

        SEARCH_SOURCES = ("with_identifier", "with_env", "with_config_file", "with_name")
        REQUIRE_OPS = {"find_one", "find_all"}
        EXCLUSIVE_OPS = {"find_one", "find_all"}
        EXPECTED_SOURCES = {"find_one": 1, "find_all": 0}

        if EXCLUSIVE_OPS.issubset(calls_set):
            raise ValueError("find_one() and find_all() cannot be used together in the same pipeline.")

        if op not in EXPECTED_SOURCES:
            return self

        if op in REQUIRE_OPS and "with_organization_name" not in calls_set:
            raise ValueError(f"{op}() requires: with_organization_name().")

        source_usage = {
            "with_identifier": "with_identifier" in calls_set,
            "with_env": "with_env" in calls_set,
            "with_config_file": "with_config_file" in calls_set,
            "with_name": "with_name" in calls_set
        }
        used_sources = [name for name, used in source_usage.items() if used]
        expected = EXPECTED_SOURCES[op]

        if len(used_sources) != expected:
            msg = self._format_source_error(op, used_sources, SEARCH_SOURCES)
            raise ValueError(msg)

        return self


    def _format_source_error(self, method: str, used_sources: list[str], all_sources: tuple[str, ...]) -> str:
        if method == "find_all":
            return (
                "find_all() cannot be combined with search sources: "
                f"{', '.join(sorted(used_sources))}. Use find_one() if you need those."
            )
        if not used_sources:
            return f"find_one() requires exactly one of: {', '.join(all_sources)}."
        return (
            "find_one() cannot combine multiple search sources at once. "
        )








