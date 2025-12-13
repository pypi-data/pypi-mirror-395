from dlt.common.schema.utils import dlt_load_id_column, new_table
from dlt.common.schema.typing import TTableSchema


DLT_DATA_QUALITY_PIPELINE_NAME_TEMPLATE = "_dlt_dq_{dataset_name}"
DLT_CHECKS_RESULTS_TABLE_NAME = "_dlt_check_results"
DLT_DATA_QUALITY_SCHEMA_NAME = "_dlt_data_quality"
QUALIFIED_CHECK_NAME_COL = "check_qualified_name"
TABLE_NAME_COL = "table_name"
ROW_COUNT_COL = "row_count"
CHECK_COUNT_COL = "check_count"
CHECK_SUCCESS_COUNT_COL = "success_count"
CHECK_SUCCESS_RATE_COL = "success_rate"


def checks_results_table() -> TTableSchema:
    table = new_table(
        table_name=DLT_CHECKS_RESULTS_TABLE_NAME,
        columns=[
            dlt_load_id_column(),
            {
                "name": QUALIFIED_CHECK_NAME_COL,
                "data_type": "text",
                "description": (
                    "Unique identifier for the check. It is typically composed of a table"
                    " name, a column name, a check name, and check argument identifier."
                ),
            },
            {
                "name": TABLE_NAME_COL,
                "data_type": "text",
                "description": (
                    "Table for which results apply." " Is null for dataset-level checks"
                ),
                "nullable": True,
            },
            {
                "name": ROW_COUNT_COL,
                "data_type": "bigint",
                "description": (
                    "Number of rows involved in this check." " Is null for dataset-level checks."
                ),
                "nullable": True,
            },
            {
                "name": CHECK_SUCCESS_COUNT_COL,
                "data_type": "bigint",
                "description": (
                    "Number of rows succeeding the check."
                    " Is null for table and dataset-level checks."
                ),
                "nullable": True,
            },
            {
                "name": CHECK_SUCCESS_RATE_COL,
                "data_type": "double",
                "description": (
                    "Number of rows succeeding the check."
                    " Is null for table and dataset-level checks."
                ),
                "nullable": False,
            },
            # {
            #     "name": LOAD_IDS_CHECKED_COL,
            #     "data_type": "json",
            #     "description": (
            #         "List of `_dlt_load_id` values that were included when running checks."
            #     ),
            #     "nullable": False,
            # },
        ],
        write_disposition="append",
    )

    return table
