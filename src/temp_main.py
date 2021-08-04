import logging

import pandas as pd
from schema_parser import parse_schema
from schema_validator import schema_validator

logger = logging.getLogger()


# create inputs
df = pd.DataFrame()
json_file = "sample.json"

# initialize
loaded_schema = parse_schema(json_file)

loaded_validator = schema_validator(df, loaded_schema)

loaded_validator.column_name_validate()
loaded_validator.data_type_validate()
loaded_validator.non_null_validate()
loaded_validator.naturalPrimaryKey_validate()

validation_result = loaded_validator.validation_result

for key, value in validation_result.items():

    if value[0] == False:
        logger.info(
            f"VALIDATION FAILED FOR: '{key}'\n With validation values:\n {value}"
        )
        print(None)
