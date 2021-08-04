import json
import logging
import sys
from copy import deepcopy

import pandas as pd


class parse_schema:

    # TEMP: Research how to build a standard json schema and validate developer defined json schema\
    # with a fixed meta-schema file
    # https://python-jsonschema.readthedocs.io/en/latest/
    required_keys = (
        "name",
        "type",
        "doc",
        "naturalPrimaryKey",
        "compositePrimaryKey",
        "fields",
    )

    def __init__(self, schema_file: str):

        with open(schema_file) as f:
            self.schema = json.load(f)
        self.schema_file = schema_file

    def _validate_json_schema(self):

        """validate schema file with a template schema"""
        key_match = sorted(parse_schema.required_keys) == sorted(
            tuple(self.schema.keys())
        )
        if key_match:
            logger.info(
                f"provided schema is valid {self.schema_file} \
                validated for primary keys"
            )
        else:
            logger.info(
                f"provided schema is InValid {self.schema_file} \
                failed validation for primary keys"
            )
            sys.exit(1)
        return None

    def _name(self):
        return self.schema["name"]

    def _type(self):
        return self.schema["type"]

    def _doc(self):
        return self.schema["doc"]

    def naturalPrimaryKey(self):
        primary_keys = self.schema["naturalPrimaryKey"]
        return [i["name"] for i in primary_keys]

    def compositePrimaryKey(self):
        return self.schema["compositePrimaryKey"]

    def fields(self):
        return self.schema["fields"]

    def dtypes_array(self):

        fields = self.fields()
        dtypes_arr = {}
        for i in fields:
            try:
                dtypes_arr[i["name"]] = i["type"]
            except KeyError as k:
                logger.info(
                    f"Missing a Required Field Key in Schema for: \
                    {self.schema_file} AT {i}"
                )
                raise k
        return dtypes_arr

    def dtypes_flattened(self):

        """dtypes without 'null'"""
        dtypes_arr = self.dtypes_array()
        dtypes_flat = deepcopy(dtypes_arr)
        for i in dtypes_flat:
            if "null" in dtypes_flat[i]:
                dtypes_flat[i].remove("null")
        return dtypes_flat

    def columns(self):
        return list(self.dtypes_array().keys())

    def non_null_columns(self):
        columns = self.dtypes_array()
        return [i for i in columns if "null" not in columns[i]]
