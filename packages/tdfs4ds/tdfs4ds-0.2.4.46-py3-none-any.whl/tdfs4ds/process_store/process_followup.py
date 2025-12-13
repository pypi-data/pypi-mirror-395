import tdfs4ds
from tdfs4ds.utils.query_management import execute_query_wrapper
import teradataml as tdml
from tdfs4ds import logger_safe, logger

@execute_query_wrapper
def follow_up_table_creation():
    """
    Creates SQL queries for the creation of a follow-up table, adding comments to the table,
    and creating a view for the table in the specified schema.

    Returns:
        list: A list of three SQL query strings - one for creating the table, one for commenting on the table,
              and one for creating a view of the table.
    """

    # SQL query to create the follow-up table with specified columns and constraints
    query_table = f"""
CREATE MULTISET TABLE {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME},
FALLBACK,
NO BEFORE JOURNAL,
NO AFTER JOURNAL,
CHECKSUM = DEFAULT,
DEFAULT MERGEBLOCKRATIO,
MAP = TD_MAP1
(
    RUN_ID         VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
    PROCESS_TYPE   VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC NOT NULL,
    PROCESS_ID     VARCHAR(255) CHARACTER SET LATIN NOT CASESPECIFIC,
    START_DATETIME TIMESTAMP(6) WITH TIME ZONE NOT NULL,
    END_DATETIME   TIMESTAMP(6) WITH TIME ZONE,
    VALIDTIME_DATE TIMESTAMP(6) WITH TIME ZONE, --VARCHAR(255) CHARACTER SET LATIN,
    APPLIED_FILTER JSON(2000),
    STATUS VARCHAR(2048) CHARACTER SET LATIN
)
PRIMARY INDEX (RUN_ID, PROCESS_ID)
    """

    # SQL query to add a comment to the follow-up table
    query_comment = f"COMMENT ON TABLE {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME} IS 'followup table of the feature store'"

    # SQL query to create a view of the follow-up table with a modified name
    query_view = f"""
REPLACE VIEW {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME.replace('FS_', 'FS_V_')} AS
LOCK ROW FOR ACCESS
SELECT *
FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME}
    """

    # Return the list of SQL queries
    return [query_table, query_comment, query_view]


@execute_query_wrapper
def followup_open(run_id, process_type, process_id, timemanager=None, filtermanager=None):
    """
    Generates an SQL query to insert a new record into the follow-up table for a given run.

    Args:
        run_id (str): The unique identifier for the run.
        process_type (str): The type of process being executed.
        process_id (str): The unique identifier for the process.
        timemanager (object, optional): An object managing time-related data. Defaults to None.
        filtermanager (object, optional): An object managing filter-related data. Defaults to None.

    Returns:
        str: The generated SQL query string.
    """

    # Determine the value of VALIDTIME_DATE based on FEATURE_STORE_TIME
    if tdfs4ds.FEATURE_STORE_TIME is None:
        VALIDTIME_DATE = 'NULL'
    else:
        VALIDTIME_DATE = "'" + tdfs4ds.FEATURE_STORE_TIME + "'"

    if process_type is None:
        process_type = 'RUN'

    # Generate SQL query when both timemanager and filtermanager are None
    if timemanager is None and filtermanager is None:
        query = f"""
INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME}
SELECT
    '{run_id}' AS RUN_ID
,   '{process_type.upper()}' AS PROCESS_TYPE
,   '{process_id}' AS PROCESS_ID
,   CURRENT_TIME AS START_DATETIME
,   NULL AS END_DATETIME
,   {VALIDTIME_DATE} AS VALIDTIME_DATE
,   NULL AS APPLIED_FILTER
,   'RUNNING' AS STATUS
"""
    # Generate SQL query when timemanager is None and filtermanager is not None
    elif timemanager is None:
        query = f"""
INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME}
SELECT
    '{run_id}' AS RUN_ID
,   '{process_type.upper()}' AS PROCESS_TYPE
,   '{process_id}' AS PROCESS_ID
,   CURRENT_TIME AS START_DATETIME
,   NULL AS END_DATETIME
,   {VALIDTIME_DATE} AS VALIDTIME_DATE
,   FILTER_MANAGER.APPLIED_FILTER
,   'RUNNING' AS STATUS
FROM (SELECT
    JSON_AGG({','.join(filtermanager.col_names)}) AS APPLIED_FILTER
    FROM {filtermanager.schema_name}.{filtermanager.view_name}) FILTER_MANAGER
"""
    # Generate SQL query when filtermanager is None and timemanager is not None
    elif filtermanager is None:
        query = f"""
INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME}
SELECT
    '{run_id}' AS RUN_ID
,   '{process_type.upper()}' AS PROCESS_TYPE
,   '{process_id}' AS PROCESS_ID
,   CURRENT_TIME AS START_DATETIME
,   NULL AS END_DATETIME
,   TIME_MANAGER.BUSINESS_DATE AS VALIDTIME_DATE
,   NULL AS APPLIED_FILTER
,   'RUNNING' AS STATUS
FROM {timemanager.schema_name}.{timemanager.view_name} TIME_MANAGER
"""
    # Generate SQL query when both timemanager and filtermanager are not None
    else:
        query = f"""
INSERT INTO {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME}
SELECT
    '{run_id}' AS RUN_ID
,   '{process_type.upper()}' AS PROCESS_TYPE
,   '{process_id}' AS PROCESS_ID
,   CURRENT_TIME AS START_DATETIME
,   NULL AS END_DATETIME
,   TIME_MANAGER.BUSINESS_DATE AS VALIDTIME_DATE
,   FILTER_MANAGER.APPLIED_FILTER
,   'RUNNING' AS STATUS
FROM {timemanager.schema_name}.{timemanager.view_name} TIME_MANAGER,
(SELECT
    JSON_AGG({','.join(filtermanager.col_names)}) AS APPLIED_FILTER
    FROM {filtermanager.schema_name}.{filtermanager.view_name}) FILTER_MANAGER
"""

    return query


@execute_query_wrapper
def followup_close(run_id, process_type, process_id, status='COMPLETED', filtermanager=None):
    """
    Generates an SQL query to update the status and end time of a specific process run
    in the follow-up table.

    Args:
        run_id (str): The unique identifier for the run.
        process_type (str): The type of process being executed.
        process_id (str): The unique identifier for the process.
        status (str, optional): The status to set for the process run. Defaults to 'COMPLETED'.

    Returns:
        str: The generated SQL query string.
    """

    # SQL query to update the status and end datetime of the specified run
    if filtermanager is None:
        query = f"""
    UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME}
    SET
        STATUS       = '{status}',
        END_DATETIME = CURRENT_TIME
    WHERE
        RUN_ID       = '{run_id}'
    AND PROCESS_TYPE = '{process_type.upper()}'
    AND PROCESS_ID   = '{process_id}'
    AND STATUS       = 'RUNNING'
    """
    else:
        # there is a filter manager
        query = f"""
    UPDATE {tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME}
    FROM (SELECT
            JSON_AGG({','.join(filtermanager.col_names)}) AS APPLIED_FILTER
            FROM {filtermanager.schema_name}.{filtermanager.view_name}) FILTER_MANAGER
    SET
        STATUS       = '{status}',
        END_DATETIME = CURRENT_TIME
    WHERE
        RUN_ID         = '{run_id}'
    AND PROCESS_TYPE   = '{process_type.upper()}'
    AND PROCESS_ID     = '{process_id}'
    AND CAST(FS_FOLLOW_UP.APPLIED_FILTER AS VARCHAR(20000) )= CAST(FILTER_MANAGER.APPLIED_FILTER AS VARCHAR(20000))
    AND STATUS         = 'RUNNING'
    """

    if status.startswith('FAIL'):
        raise
    return query

from typing import Optional

def follow_up_report(filtermanager: Optional[object] = None, process_id: Optional[str] = None):
    """
    Return a follow-up report as a `tdml.DataFrame`, optionally filtered by
    `process_id` and/or a `filtermanager`'s applied filter.

    Behavior by arguments:
        - process_id is None and filtermanager is None:
            Return all rows from SCHEMA.FOLLOW_UP_NAME, sorted by START_DATETIME desc.
        - process_id is not None and filtermanager is None:
            Return rows for the given PROCESS_ID.
        - process_id is not None and filtermanager is not None:
            Return rows for the given PROCESS_ID whose APPLIED_FILTER matches the
            JSON_AGG of `filtermanager`'s columns coming from its schema/view.
        - process_id is None and filtermanager is not None:
            Return rows whose APPLIED_FILTER matches the JSON_AGG of `filtermanager`
            (no PROCESS_ID constraint).

    Args:
        filtermanager: An object exposing `col_names`, `schema_name`, and `view_name`.
            Its columns are aggregated via `JSON_AGG(col1, col2, ...)` to compare
            against A.APPLIED_FILTER.
        process_id: Optional process identifier used to filter by PROCESS_ID.

    Returns:
        tdml.DataFrame: The resulting dataframe sorted by START_DATETIME (descending).

    Raises:
        ValueError: If `filtermanager` is provided but is missing required attributes
            or has an empty `col_names` list.
        RuntimeError: If the query fails.
    """
    logger_safe("debug", "follow_up_report called with process_id=%s, filtermanager=%s",
                process_id, type(filtermanager).__name__ if filtermanager else None)

    table_fqn = f"{tdfs4ds.SCHEMA}.{tdfs4ds.FOLLOW_UP_NAME}"

    # Case 1: No filters at all -> return full table
    if process_id is None and filtermanager is None:
        logger_safe("info", "Returning all follow-up rows (no filters).")
        try:
            return tdml.DataFrame(tdml.in_schema(tdfs4ds.SCHEMA, tdfs4ds.FOLLOW_UP_NAME)) \
                      .sort('START_DATETIME', ascending=False)
        except Exception as e:
            logger_safe("error", "Failed to fetch all follow-up rows: %s", e)
            raise RuntimeError("Database query failed while fetching follow-up report.") from e

    # Helper to build the FILTER_MANAGER scalar subquery when filtermanager is provided
    def _build_filter_manager_subquery(fm: object) -> str:
        required_attrs = ("col_names", "schema_name", "view_name")
        if not all(hasattr(fm, a) for a in required_attrs):
            raise ValueError("filtermanager must have col_names, schema_name, and view_name.")
        if not getattr(fm, "col_names", None):
            raise ValueError("filtermanager.col_names must be a non-empty list.")

        json_cols = ",".join(fm.col_names)
        subq = f"""
            (
                SELECT JSON_AGG({json_cols}) AS APPLIED_FILTER
                FROM {fm.schema_name}.{fm.view_name}
            ) FILTER_MANAGER
        """
        logger_safe("debug", "Constructed FILTER_MANAGER subquery with columns: %s", json_cols)
        return subq

    # Defensive escaping for process_id if used in a literal (prefer bind params if available)
    def _escape_literal(val: str) -> str:
        return val.replace("'", "''")

    try:
        # Case 2: process_id only
        if process_id is not None and filtermanager is None:
            pid = _escape_literal(process_id)
            query = f"""
                SELECT *
                FROM {table_fqn}
                WHERE PROCESS_ID = '{pid}'
            """
            logger_safe("info", "Fetching follow-up rows filtered by PROCESS_ID only.")
            return tdml.DataFrame.from_query(query).sort('START_DATETIME', ascending=False)

        # Case 3: filtermanager only
        if process_id is None and filtermanager is not None:
            subq = _build_filter_manager_subquery(filtermanager)
            query = f"""
                SELECT A.*
                FROM {table_fqn} A,
                     {subq}
                WHERE CAST(A.APPLIED_FILTER AS VARCHAR(20000)) =
                      CAST(FILTER_MANAGER.APPLIED_FILTER AS VARCHAR(20000))
            """
            logger_safe("info", "Fetching follow-up rows filtered by FILTER_MANAGER only.")
            return tdml.DataFrame.from_query(query).sort('START_DATETIME', ascending=False)

        # Case 4: both process_id and filtermanager
        pid = _escape_literal(process_id)  # type: ignore[arg-type]
        subq = _build_filter_manager_subquery(filtermanager)  # type: ignore[arg-type]
        query = f"""
            SELECT A.*
            FROM {table_fqn} A,
                 {subq}
            WHERE A.PROCESS_ID = '{pid}'
              AND CAST(A.APPLIED_FILTER AS VARCHAR(20000)) =
                  CAST(FILTER_MANAGER.APPLIED_FILTER AS VARCHAR(20000))
        """
        logger_safe("info", "Fetching follow-up rows filtered by PROCESS_ID and FILTER_MANAGER.")
        return tdml.DataFrame.from_query(query).sort('START_DATETIME', ascending=False)

    except Exception as e:
        logger_safe("error", "Failed to fetch follow-up report: %s", e)
        raise RuntimeError("Database query failed while fetching follow-up report.") from e
