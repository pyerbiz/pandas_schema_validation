# pandas_schema_validation

This tool takes runs validation checks against a pandas dataframe, by refering to a json file created by developer. This helps in setting the schema of a dataframe before running the actual data processing. This is very useful for fixing the schema's of your data processing tasks (data pipelines) -- avoid a lot of bugs that come up as schema evolves with time.

The idea is to treat pandas dataframes as relations in a relational database. Hence be able apply stringent schema requirements on your data pipeline for a new data processing task in the pipeline.
