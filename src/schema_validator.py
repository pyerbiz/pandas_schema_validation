import pandas as pd


class schema_validator:

    validation_result = dict()

    def __init__(self, df: pd.DataFrame(), parsed_schema: str):
        self.parsed_schema = parsed_schema
        self.df = df

    def column_name_validate(self):

        df_cols = sorted(list(self.df.columns))
        schema_cols = sorted(self.parsed_schema.columns())
        validated = df_cols == schema_cols
        validation_params = (validated, df_cols, schema_cols)

        self.validation_result["column_name_validate"] = validation_params

    def data_type_validate(self):

        defined_dtypes = self.parsed_schema.dtypes_flattened()

        inferred_dtypes = dict()
        for col in self.df:
            dtype = pd.api.types.infer_dtype(self.df[col])
            inferred_dtypes[col] = [dtype]
        validated = defined_dtypes == inferred_dtypes
        validation_params = (validated, inferred_dtypes, defined_dtypes)
        self.validation_result["data_type_validate"] = validation_params

    def non_null_validate(self):

        non_null_cols = self.parsed_schema.non_null_columns()
        failed_cols = []
        for col in non_null_cols:
            has_null = self.df[col].isnull().values.any()
            if has_null:
                failed_cols.append(col)
            else:
                pass

        if len(failed_cols) > 0:
            validated = False
        else:
            validated = True

        validation_params = (validated, failed_cols)
        self.validation_result["non_null_validate"] = validation_params

    def naturalPrimaryKey_validate(self):

        # Can return duplicate subset df later
        list_of_primary_keys = self.parsed_schema.naturalPrimaryKey()
        keys = {}
        for i in list_of_primary_keys:
            i_validated = self.df[i].duplicated().any()
            keys[i] = i_validated

        validated = False in keys.values()
        validation_params = (validated, keys)

        self.validation_result["naturalPrimaryKey_validate"] = validation_params

    def compositePrimaryKey_validate(self):
        # TODO
        pass
