from opengate_data.searching.search import SearchBuilder
from requests import Response
from opengate_data.utils.utils import send_request, set_method_call, parse_json, validate_type, handle_exception, handle_error_response
import os
import pandas as pd


class FindDatasetsBuilder():
    """ Find Datasets Builder """

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
    def with_organization_name(self, organization_name: str) -> 'FindDatasetsBuilder':
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
    def with_format(self, format_data: str) -> 'FindDatasetsBuilder':
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
        validate_type(format_data, str, "Format data")
        self.format_data = format_data
        return self
    
    @set_method_call
    def with_identifier(self, identifier: str) -> 'FindDatasetsBuilder':
        """
        set the dataset identifier.

        Args:
            identifier (str): The identifier of the dataset.

        Returns:
            FindDatasetsBuilder: Returns itself to allow for method chaining.

        Example:
            ~~~python
                builder.with_identifier("dataset_id")
            ~~~
        """
        validate_type(identifier, str, "Find identifier")
        self.identifier = identifier
        return self
    
    @set_method_call
    def with_config_file(self, config_file: str, section: str, config_key: str, prefer: str = "auto") -> 'FindDatasetsBuilder':
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
        self.config_prefer = prefer  # por defecto 'auto'

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
    def with_name(self, find_name: str) -> 'FindDatasetsBuilder':
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
    def with_env(self, env_key: str, prefer: str = "auto") -> 'FindDatasetsBuilder':
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
        self.env_prefer = prefer  # por defecto 'auto'
        return self


    @set_method_call
    def find_all(self) -> 'FindDatasetsBuilder':
        """
        Searches for all available data sets resources.

        Returns:
            FindDatasetsBuilder: Returns the current instance to allow method chaining.

        Example:
            ~~~python
                builder.with_organization_name('my_organization').find_all()
            ~~~
        """
        self.method = 'find_all'
        return self

    @set_method_call
    def find_one(self) -> 'FindDatasetsBuilder':
        """
        Searches for a single transformer resource by its identifier.

        This method prepares the request to find a specific transformer based on its identifier. The identifier is obtained automatically if not explicitly defined or can be obtained from a configuration file or environment variables.

        Returns:
            FindDatasetsBuilder: Returns the current instance to allow method chaining.

        Example:
            ~~~python
                builder.with_organization_name('my_organization').with_organization_name("organization_name").with_format("dict").with_identifier("identifier").find_one().build().execute()
            ~~~
        """
        self.method = 'find_one'
        return self
    
    @set_method_call
    def build(self) -> 'FindDatasetsBuilder':
        """
        Finalizes the construction of the IoT collection configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

        Returns:
            FindDatasetsBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

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
        Executes the data sets search immediately after building the configuration.

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
                raise Exception(
                    "The build() function must be the last method invoked before execute.")

        if 'build' not in self.method_calls and 'build_execute' not in self.method_calls:
            raise Exception(
                "You need to use a build() or build_execute() function the last method invoked before execute.")

        self._validate_builds()

        self.url = f'{self.base_url}/v80/datasets/provision/organizations/{self.organization_name}'

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
            response = send_request(method='get', headers=self.client.headers, url=self.url)
            status_code = getattr(response, 'status_code')
            if status_code != 200:
                return handle_error_response(response)
            data = response.json()
        except Exception as e:
            return handle_exception(e)

        datasets = data.get('datasets', [])
        if not isinstance(datasets, list):
            raise ValueError("Unexpected format: 'datasets' is not a list.")

        by_id = {d.get("identifier"): d for d in datasets if isinstance(d, dict)}
        by_name = {d.get("name"): d for d in datasets if isinstance(d, dict)}

        def get_by_id(value: str) -> dict:
            ds = by_id.get(value)
            if not ds:
                raise ValueError(f"Data set with identifier '{value}' not found.")
            return ds

        def get_by_name(value: str) -> dict:
            ds = by_name.get(value)
            if not ds:
                raise ValueError(f"Data set with name '{value}' not found.")
            return ds

        def auto_lookup(value: str) -> dict:
            if value in by_id:
                return by_id[value]
            if value in by_name:
                return by_name[value]
            raise ValueError(f"Data set '{value}' not found by identifier or name.")

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
                return handle_error_response(response)
                
            if self.format_data == 'dict':
                return response.json()

            if self.format_data == 'pandas':
                return pd.json_normalize(response.json()['datasets'])

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