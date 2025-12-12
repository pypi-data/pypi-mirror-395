from opengate_data.utils.utils import validate_type


class SelectBuilder:
    """
    A flexible builder for constructing SELECT clauses for several OpenGate entities.

    This builder supports three independent modes, which cannot be mixed
    inside the same instance:

    1. **Simple mode** (Datasets, Timeseries search):
        - `.add("field_name")`
        - Produces: ["field1", "field2", ...]

    2. **Extended mode** (Structured search):
        - `.add("path.to.resource", ["field", ("other", "alias")])`
        - Produces:
            [
              { "name": "...", "fields": [{ "field": "...", "alias": "..." }] }
            ]

    3. **Column mode** (Timeseries EXPORT):
        - `.add_column("FIRST")`
        - `.add_column("bucket_id", output={"parquet": {"type": "INT"}})`
        - Produces:
            [
              { "column": "FIRST" },
              { "column": "bucket_id", "output": {...} }
            ]

    You cannot mix modes. Each builder instance must use only one mode.

    Examples:
        Simple mode:
            SelectBuilder().add("Gross").add("Temp")

        Extended mode:
            SelectBuilder().add("provision.device.identifier",
                                [("value", "id"), "date"])

        Column mode (Timeseries Export):
            SelectBuilder().add_column("FIRST").add_column("LAST")

    Use `.build()` to retrieve the final SELECT list.
    """

    def __init__(self):
        self._select_fields = []
        self._mode = None
    def add(self, name: str, fields=None):
        """
        Add a SELECT entry in either simple or extended mode.

        Args:
            name (str): Field name (simple mode) or entity name (extended mode).
            fields (list, optional): Only for extended mode; list of strings or
                                     tuples (field, alias).

        Returns:
            SelectBuilder: fluent API.
        """
        validate_type(name, str, "name")

        # Simple mode
        if fields is None:
            if self._mode is None:
                self._mode = "simple"
            elif self._mode != "simple":
                raise ValueError("Cannot mix simple and extended select modes")

            if name not in self._select_fields:
                self._select_fields.append(name)
            return self

        #  Extended mode 
        if self._mode is None:
            self._mode = "extended"
        elif self._mode != "extended":
            raise ValueError("Cannot mix simple and extended select modes")

        validate_type(fields, list, "fields")

        processed_fields = []
        for field in fields:
            if isinstance(field, str):
                processed_fields.append({"field": field})
            elif isinstance(field, tuple):
                validate_type(field[0], str, "field[0]")
                entry = {"field": field[0]}
                if len(field) > 1:
                    validate_type(field[1], str, "field[1]")
                    entry["alias"] = field[1]
                processed_fields.append(entry)
            else:
                raise ValueError("Each field must be a string or a tuple")

        existing = next((e for e in self._select_fields if e["name"] == name), None)

        if existing:
            for pf in processed_fields:
                if pf not in existing["fields"]:
                    existing["fields"].append(pf)
        else:
            self._select_fields.append({"name": name, "fields": processed_fields})

        return self

    def add_column(self, column_name: str, output: dict | None = None):
        """
        Add a Timeseries Export column entry.

        Produces backend-compatible objects like:
            { "column": "FIRST" }
            { "column": "bucket_id", "output": {...} }

        Args:
            column_name (str): Name of the export column.
            output (dict, optional): Optional output descriptor such as:
                { "parquet": { "type": "INT" } }
                { "name": "serial_number", "parquet": { "type": "STRING" } }

        Returns:
            SelectBuilder: fluent API.
        """
        validate_type(column_name, str, "column")

        # Enforce mode consistency
        if self._mode is None:
            self._mode = "column"
        elif self._mode != "column":
            raise ValueError("Cannot mix different SELECT modes in the same SelectBuilder")

        entry = {"column": column_name}
        if output is not None:
            validate_type(output, dict, "output")
            entry["output"] = output

        self._select_fields.append(entry)
        return self

    def build(self):
        """
        Return the constructed SELECT list.

        Raises:
            ValueError: If no select elements were added.

        Returns:
            list: Dicts (column mode), strings (simple mode) or dicts (extended mode).
        """
        if not self._select_fields:
            raise ValueError("No select criteria have been added")

        return self._select_fields
