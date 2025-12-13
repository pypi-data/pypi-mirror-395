import teradataml as tdml
import tdfs4ds
from teradataml.context.context import _get_database_username
from tdfs4ds.utils.visualization import display_table
from tdfs4ds.utils.query_management import execute_query
from tdfs4ds.utils.info import seconds_to_dhms
import time
import re
import pandas as pd
from tdfs4ds import logger_safe, logger


def generate_on_clause(entity_id, entity_null_substitute, left_name, right_name):
    res = []
    for k in entity_id.keys():
        if 'varchar' in entity_id[k] and k in entity_null_substitute.keys():
            res.append(
                f"COALESCE({left_name}.{k},'{entity_null_substitute[k]}') = COALESCE({right_name}.{k},'{entity_null_substitute[k]}')")
        elif k in entity_null_substitute.keys():
            res.append(
                f"COALESCE({left_name}.{k},{entity_null_substitute[k]}) = COALESCE({right_name}.{k},{entity_null_substitute[k]})")
        else:
            res.append(f"{left_name}.{k} = {right_name}.{k}")

    return '\nAND '.join(res)


def generate_collect_stats(entity_id, primary_index='', partitioning=''):
    """
    Generate a COLLECT STATISTICS SQL query based on specified entity identifiers, primary index,
    and partitioning information. The query collects statistics for columns relevant to the data
    structure, including partitioning and entity identifiers, for optimized query performance.

    Parameters:
    entity_id (list or dict): A list of entity IDs or a dictionary where keys represent entity IDs.
                              Used to identify the columns requiring statistical collection.
    primary_index (str or list, optional): The primary index column(s) for the table, provided as
                                           a single string or list of strings. Defaults to an empty string.
    partitioning (str, optional): A string defining partitioning information, used to identify
                                  additional columns for statistical collection. Defaults to an empty string.

    Returns:
    tuple: A tuple containing two strings:
           - The base COLLECT STATISTICS SQL query.
           - The extended COLLECT STATISTICS SQL query with sampling and thresholds applied.
    """

    # Convert entity_id dictionary keys to a list if it's provided as a dictionary
    if isinstance(entity_id, dict):
        entity_id_list = list(entity_id.keys())
    else:
        entity_id_list = entity_id

    # Sort entity ID list and primary_index once to ensure consistent order
    entity_id_list.sort()
    if isinstance(primary_index, str):
        primary_index = [primary_index]
    primary_index.sort()

    # Identify partitioning columns that match any entity IDs using case-insensitive search
    partitioning_names = [k for k in entity_id_list if
                          re.search(r'\b' + re.escape(k.upper()) + r'\b', partitioning.upper())]

    # Include 'FEATURE_ID' as a default partitioning column for statistics collection
    partitioning_names = list(set(partitioning_names + ['FEATURE_ID']))

    # Initialize the base query with statistics collection on the PARTITION column
    query = ['COLLECT STATISTICS COLUMN(PARTITION)']

    # Append additional partitioning columns, if any, to the base query
    query += ['COLUMN(' + c + ')' for c in partitioning_names]

    # Add fixed columns that are always included in the statistics collection
    query.extend(['COLUMN(FEATURE_VERSION)', 'COLUMN(ValidStart)', 'COLUMN(ValidEnd)'])

    # Initialize the extended query with sampling and threshold settings for statistics collection
    query_extension_header = 'COLLECT STATISTICS USING SAMPLE 25 PERCENT AND THRESHOLD 15 PERCENT'
    query_extension        = []

    # Add primary index columns to the extended query
    if primary_index:
        query_extension.append(f"COLUMN({','.join(primary_index)})")

    # Include entity ID columns in the extended query if they differ from the primary index columns
    if entity_id_list != primary_index:
        query_extension.append(f"COLUMN({','.join(entity_id_list)})")

    # Join the base and extended query parts with a newline separator and return as a tuple
    if len(query_extension) > 0:
        return '\n,'.join(query), query_extension_header + '\n' + '\n,'.join(query_extension)
    else:
        return '\n,'.join(query), None

def get_feature_id_and_conversion(list_entity_id, feature_names):
    """
    Fetch feature ID and conversion mapping from feature catalog.

    Parameters:
    - list_entity_id: List of entity IDs.
    - feature_names: List of feature names.

    Returns:
    - feature_id_names: List of tuples containing feature details (FEATURE_ID, FEATURE_NAME, FEATURE_TABLE, FEATURE_DATABASE).
    - conversion_name2id: Dictionary mapping FEATURE_NAME to FEATURE_ID.
    """
    ENTITY_ID__ = ','.join([k for k in list_entity_id])
    FEATURE_NAMES__ = ','.join([f"'{k}'" for k in feature_names])

    query = f"""
    SELECT FEATURE_ID, FEATURE_NAME, FEATURE_TABLE, FEATURE_DATABASE
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW}
    WHERE DATA_DOMAIN = '{tdfs4ds.DATA_DOMAIN}'
    AND ENTITY_NAME = '{ENTITY_ID__}'
    AND FEATURE_NAME IN ({FEATURE_NAMES__})
    """

    # Execute the query
    feature_id_names = tdml.execute_sql(query).fetchall()

    # Debugging information
    if tdfs4ds.DEBUG_MODE:
        print('--- prepare_feature_ingestion ---')
        print('feature_id_names:', feature_id_names)

    # Create the mapping
    conversion_name2id = {x[1]: x[0] for x in feature_id_names}

    return feature_id_names, conversion_name2id

def prepare_feature_ingestion(df, entity_id, feature_names, feature_versions=None, primary_index=None, partitioning = '', entity_null_substitute={}, **kwargs):
    """
    Transforms and prepares a DataFrame for feature ingestion into a feature store by unpivoting it.

    This function accepts a DataFrame along with the specifications for entity IDs, feature names, and optionally,
    feature versions. It generates a new DataFrame with the data unpivoted to align with the requirements of a feature
    store ingestion process. Additionally, it creates a volatile table in the database to facilitate the transformation.

    Parameters:
    - df (tdml.DataFrame): The input DataFrame containing the feature data.
    - entity_id (list/dict/other): Specifies the entity IDs. If a dictionary, the keys are used as entity IDs.
                                   If a list or another type, it is used directly as the entity ID.
    - feature_names (list): Names of features to be unpivoted.
    - feature_versions (dict, optional): Maps feature names to their versions. If not provided, a default version is applied.
    - primary_index (list/str, optional): Primary index(es) for the volatile table. If not specified, entity IDs are used.
    - **kwargs: Additional keyword arguments for customization.

    Returns:
    tuple: A tuple containing:
           1. A tdml.DataFrame with the transformed data ready for ingestion.
           2. The name of the volatile table created in the database.

    Raises:
    Exception: If the function encounters an issue during the database operations or data transformations.

    Note:
    - The function handles different data types for 'entity_id' to ensure correct SQL query formation.
    - It assumes a specific structure for 'df' to properly execute SQL commands for data transformation.

    Example:
    >>> df = tdml.DataFrame(...)
    >>> entity_id = {'customer_id': 'INTEGER'}
    >>> feature_names = ['feature1', 'feature2']
    >>> transformed_df, volatile_table_name = prepare_feature_ingestion(df, entity_id, feature_names)
    """

    # Record the start time
    start_time = time.time()

    # Normalize entity_id into a list of keys
    if isinstance(entity_id, list):
        list_entity_id = entity_id
    elif isinstance(entity_id, dict):
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]
    list_entity_id.sort()

    feature_id_names, conversion_name2id = get_feature_id_and_conversion(list_entity_id, feature_names)

    features_infos = pd.DataFrame(feature_id_names, columns=['FEATURE_ID', 'FEATURE_NAME', 'FEATURE_TABLE', 'FEATURE_DATABASE'])
    features_infos['FEATURE_VERSION'] = [feature_versions[k] for k in features_infos.FEATURE_NAME.values]

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "--- prepare_feature_ingestion ---")
        logger_safe("debug", "conversion_name2id=%s", conversion_name2id)
        logger_safe("debug", "feature_names=%s", feature_names)

    # UNPIVOT mapping
    unpivot_columns = ", \n".join([f"({x}) as '{conversion_name2id[x]}'" for x in feature_names])

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "unpivot_columns=%s", unpivot_columns)

    # Output columns for volatile table
    output_columns = ', \n'.join(list_entity_id + ['CAST(FEATURE_ID AS BIGINT) AS FEATURE_ID', 'FEATURE_VALUE'])

    # Primary index
    if primary_index is None:
        primary_index = ','.join(list_entity_id)
    else:
        if not isinstance(primary_index, list):
            primary_index = [primary_index]
        primary_index = ','.join(primary_index)

    # Feature versions (defaults)
    versions = {f: tdfs4ds.FEATURE_VERSION_DEFAULT for f in feature_names}
    if feature_versions is not None:
        for k, v in feature_versions.items():
            versions[k] = v

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "versions=%s", versions)

    # CASE statement for versions
    version_query = ["CASE"] + [f"WHEN FEATURE_ID = '{conversion_name2id[k]}' THEN '{v}' " for k, v in versions.items()] + ["END AS FEATURE_VERSION"]
    version_query = '\n'.join(version_query)

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "version_query=%s", version_query)

    # Volatile table name
    volatile_table_name = df._table_name.split('.')[1].replace('"', '')
    volatile_table_name = f"temp_{volatile_table_name}"

    # Normalize entity_id again for var casting
    if isinstance(entity_id, list):
        list_entity_id = entity_id
    elif isinstance(entity_id, dict):
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Character set handling / pass-through
    res = {x.split()[0]: ''.join(x.split()[1::]) for x in str(df[feature_names].tdtypes).split('\n')}
    var_temp2 = []
    for k, v in res.items():
        if 'UNICODE' in v:
            var_temp2.append(f'{k}')
        elif 'LATIN' in v:
            var_temp2.append(f'TRANSLATE({k} USING LATIN_TO_UNICODE) AS {k}')
        else:
            var_temp2.append(f'CAST({k} AS VARCHAR(2048) CHARACTER SET UNICODE) AS {k}')
    var_temp2 = ', \n'.join(var_temp2)

    # NOTE: the original code overrides var_temp2 with just the raw column names.
    # Preserve that behavior to avoid functional change.
    var_temp2 = ', \n'.join(list(res.keys()))

    # Null substitution on entity keys
    var_temp3 = []
    for e in list_entity_id:
        if e in entity_null_substitute.keys():
            if isinstance(entity_null_substitute[e], str):
                var_temp3.append(f"coalesce({e},'{entity_null_substitute[e]}') AS {e}")
            else:
                var_temp3.append(f"coalesce({e},{entity_null_substitute[e]}) AS {e}")
        else:
            var_temp3.append(e)
    var_temp3 = ', \n'.join(var_temp3)

    # Final nested query used (the function reassigns to plain SELECT; preserve as-is)
    nested_query = f"""
            SELECT 
            {var_temp3},
            {var_temp2}
            FROM {df._table_name}
        """

    # Duplicate check query
    output_columns_unicity = ', \n'.join(list_entity_id)
    query_test_unicity = f"""
    SELECT sum(CASE WHEN n>1 THEN 1 ELSE 0 END) AS nb_duplicates
    FROM (
        SELECT 
            {output_columns_unicity},
            count(*) as n
        FROM {_get_database_username()}.{volatile_table_name}
        GROUP BY {output_columns_unicity}
    ) A
    """

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "var_temp2=%s", var_temp2)
        logger_safe("debug", "var_temp3=%s", var_temp3)
        logger_safe("debug", "nested_query=%s", nested_query)

    # Execute: create volatile table and test unicity
    try:
        tdml.DataFrame.from_query(nested_query).to_sql(
            table_name    = volatile_table_name,
            temporary     = True,
            primary_index = primary_index.split(','),
            if_exists     = 'replace'
        )
        nb_duplicates = tdml.execute_sql(query_test_unicity).fetchall()[0][0]
        if nb_duplicates is not None and nb_duplicates > 0:
            logger_safe("error", "The process generates %s duplicates", nb_duplicates)
            # Show sample duplicates in debug for troubleshooting
            if getattr(tdfs4ds, "DEBUG_MODE", False):
                sample_dups_query = f"""
                SELECT TOP 3
                    {output_columns_unicity},
                    count(*) as n
                FROM {_get_database_username()}.{volatile_table_name}
                GROUP BY {output_columns_unicity}
                HAVING n > 1
                """
                logger_safe("debug", "Sample duplicates query:\n%s", sample_dups_query)
            raise ValueError("Invalid process: the process generates duplicates.")
        # else: no duplicates
        # logger_safe("info", "No duplicate found.")  # optional
    except Exception as e:
        logger_safe("error", "prepare_feature_ingestion failed: %s", str(e).split('\n')[0])
        raise

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe(
            "debug",
            "Result volatile table dtypes:\n%s",
            tdml.DataFrame(tdml.in_schema(_get_database_username(), volatile_table_name)).tdtypes
        )

    # Timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    formatted_elapsed_time = seconds_to_dhms(elapsed_time)
    logger_safe("info", "Feature preparation for ingestion: %s (%.3fs)", formatted_elapsed_time, elapsed_time)

    # Return DataFrame and metadata
    try:
        df_out = tdml.DataFrame(tdml.in_schema(_get_database_username(), volatile_table_name))
        return df_out, volatile_table_name, features_infos
    except Exception as e:
        logger_safe("error", "Failed to materialize volatile DataFrame: %s", str(e).split()[0])
        logger_safe("error", "Feature dtypes snapshot: %s", df[feature_names].tdtypes)
        if 'TD_Unpivot contract function' in str(e).split()[0]:
            raise RuntimeError(
                "Error: you may have strings with UNICODE encoding as features; please convert them to LATIN first."
            )
        raise

    # Fallback (should not reach)
    # return None, None, None


import time
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple

import pandas as pd

def apply_collect_stats(
    entity_id: Mapping[str, Any] | Iterable[str],
    primary_index: Optional[str],
    partitioning: Optional[str],
    feature_infos: pd.DataFrame,
) -> Dict[str, Any]:
    """
    Run COLLECT STATS on all target feature tables, with fallbacks and timing.

    Steps:
    1) Determine a stable ordering of entity IDs (for deterministic query gen).
    2) Group `feature_infos` by FEATURE_DATABASE + FEATURE_TABLE to get unique targets.
    3) Generate COLLECT STATS statements via `generate_collect_stats(...)` for fallback use.
    4) For each target table:
        - Try a simple `COLLECT STATS ON <db>.<table>`.
        - On failure, retry with generated statements (and optional extension).
    5) Log a compact summary (counts + total duration) and return it as a dict.

    Parameters
    ----------
    entity_id : Mapping[str, Any] | Iterable[str]
        Entity identifiers used to parameterize collect-stat statements.
        If a mapping (e.g., dict), its *keys* are used and sorted.
        If an iterable (e.g., list/tuple), it’s sorted directly.
    primary_index : Optional[str]
        Primary index used by `generate_collect_stats` (may be None).
    partitioning : Optional[str]
        Partitioning clause used by `generate_collect_stats` (may be None).
    feature_infos : pd.DataFrame
        Must contain columns: 'FEATURE_TABLE', 'FEATURE_DATABASE', 'FEATURE_ID'.

    Returns
    -------
    Dict[str, Any]
        Summary with keys:
        - total_tables: int
        - ok: int
        - retried: int
        - failed: int
        - duration_seconds: float
        - duration_hms: str
        - details: list[dict]  # per-table status entries
    """
    # --- Validate inputs -----------------------------------------------------
    required_cols = {"FEATURE_TABLE", "FEATURE_DATABASE", "FEATURE_ID"}
    missing = required_cols.difference(feature_infos.columns)
    if missing:
        raise ValueError(f"feature_infos is missing required columns: {sorted(missing)}")

    # --- Normalize & sort entity IDs ----------------------------------------
    if hasattr(entity_id, "keys"):
        sorted_entity_ids = sorted(list(entity_id.keys()))
    else:
        sorted_entity_ids = sorted(list(entity_id))

    # --- Group to unique targets --------------------------------------------
    target_tables = (
        feature_infos[["FEATURE_TABLE", "FEATURE_DATABASE", "FEATURE_ID"]]
        .groupby(["FEATURE_TABLE", "FEATURE_DATABASE"])
        .count()
        .reset_index()
    )

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe(
            "debug",
            "collect_stats.targets | count=%s | tables=%s",
            len(target_tables),
            target_tables[["FEATURE_DATABASE", "FEATURE_TABLE"]].to_dict(orient="records"),
        )

    # --- Prepare statements --------------------------------------------------
    query_collect_stats, query_collect_stats_extension = generate_collect_stats(
        sorted_entity_ids,
        primary_index=primary_index,
        partitioning=partitioning,
    )

    # --- Execute -------------------------------------------------------------
    started = time.perf_counter()
    results: list[Dict[str, Any]] = []

    ok = retried = failed = 0

    for _, row in target_tables.iterrows():
        db = row["FEATURE_DATABASE"]
        tbl = row["FEATURE_TABLE"]
        table_fqn = f"{db}.{tbl}"

        if getattr(tdfs4ds, "DEBUG_MODE", False):
            logger_safe("debug", "collect_stats.run | table=%s", table_fqn)

        t0 = time.perf_counter()
        status = "ok"
        error_short = None
        retried_flag = False

        try:
            tdml.execute_sql(f"COLLECT STATS ON {table_fqn}")
            ok += 1
        except Exception as e:
            # First attempt failed; try generated statement(s)
            error_short = str(e).split("\n")[0]
            logger_safe("warning", "collect_stats.initial_fail | table=%s | err=%s", table_fqn, error_short)

            try:
                execute_query(query_collect_stats + f" ON {table_fqn}")
                retried_flag = True
                retried += 1

                if query_collect_stats_extension is not None:
                    execute_query(query_collect_stats_extension + f" ON {table_fqn}")
            except Exception as e2:
                status = "failed"
                error_short = str(e2).split("\n")[0]
                failed += 1
                logger_safe("error", "collect_stats.retry_fail | table=%s | err=%s", table_fqn, error_short)

        dt = time.perf_counter() - t0
        results.append(
            {
                "table": table_fqn,
                "status": status,
                "retried": retried_flag,
                "elapsed_s": dt,
                "error": error_short,
            }
        )

    # --- Final summary -------------------------------------------------------
    elapsed = time.perf_counter() - started
    formatted = seconds_to_dhms(elapsed)

    # Structured, parseable one-liner
    logger_safe(
        "info",
        "collect_stats.summary | tables=%d | ok=%d | retried=%d | failed=%d | duration=%s (%.3fs)",
        len(target_tables),
        ok,
        retried,
        failed,
        formatted,
        elapsed,
    )

    return {
        "total_tables": int(len(target_tables)),
        "ok": int(ok),
        "retried": int(retried),
        "failed": int(failed),
        "duration_seconds": float(elapsed),
        "duration_hms": formatted,
        "details": results,
    }




def _store_feature_update_insert(entity_id, volatile_table_name, entity_null_substitute={},primary_index=None,
            partitioning='', features_infos = None, **kwargs):
    """
    Stores prepared feature data in specific feature tables within a Teradata database. This function performs updates and inserts
    on the feature tables based on the provided entity IDs and prepared feature data.

    Parameters:
    - entity_id (dict): A dictionary representing the entity ID, where keys are used to identify the entity.
    - prepared_features (tdml.DataFrame): A DataFrame containing the prepared feature data for ingestion.
    - **kwargs: Additional keyword arguments that can include:
        - schema (str): The schema name where the feature tables are located.
        - feature_catalog_name (str, optional): The name of the feature catalog table, defaulting to 'FS_FEATURE_CATALOG'.

    Returns:
    None: This function does not return any value but performs database operations.

    Note:
    - The function uses the Teradata temporal feature (VALIDTIME) for handling the valid time of the records.
    - It constructs SQL queries to update existing feature values and insert new ones based on the entity ID.
    - The function handles the entity ID, feature IDs, and versions for inserting and updating records.
    - It utilizes additional settings from the tdfs4ds module for configuring the feature store time and display logs.
    - This function assumes that the necessary database tables and schema are correctly set up and accessible.

    Example Usage:
    >>> entity_id_dict = {'customer_id': 'INTEGER'}
    >>> prepared_features = tdml.DataFrame(...)
    >>> store_feature(entity_id_dict, prepared_features)
    """

    #feature_catalog = tdml.DataFrame(tdml.in_schema(tdfs4ds.SCHEMA, tdfs4ds.FEATURE_CATALOG_NAME))

    if tdfs4ds.FEATURE_STORE_TIME == None:
        validtime_statement = 'CURRENT VALIDTIME'
        validtime_statement2 = validtime_statement
    else:
        validtime_statement = f"VALIDTIME PERIOD '({tdfs4ds.FEATURE_STORE_TIME},{tdfs4ds.END_PERIOD})'"
        validtime_statement2 = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"


    sorted_entity_id = list(entity_id.keys())
    sorted_entity_id.sort()
    ENTITY_ID = ','.join([k for k in sorted_entity_id])


    # Group the target tables by feature table and feature database and count the number of occurrences
    target_tables = features_infos[['FEATURE_TABLE', 'FEATURE_DATABASE', 'FEATURE_ID']].groupby(
        ['FEATURE_TABLE', 'FEATURE_DATABASE']).count()
    if tdfs4ds.DISPLAY_LOGS:
        display_table(target_tables[['FEATURE_DATABASE', 'FEATURE_TABLE', 'FEATURE_ID']])


    ENTITY_ID = ', \n'.join([k for k in sorted_entity_id])
    #ENTITY_ID_ON = ' AND '.join([f'NEW_FEATURES.{k} = EXISTING_FEATURES.{k}' for k in sorted_entity_id])
    ENTITY_ID_ON = generate_on_clause(entity_id, entity_null_substitute, left_name='NEW_FEATURES', right_name='EXISTING_FEATURES')
    ENTITY_ID_WHERE_INS = ' OR '.join([f'EXISTING_FEATURES.{k} IS NOT NULL' for k in sorted_entity_id])
    ENTITY_ID_WHERE_UP = ' OR '.join([f'EXISTING_FEATURES.{k} IS NULL' for k in sorted_entity_id])

    ENTITY_ID_SELECT = ', \n'.join(['NEW_FEATURES.' + k for k in sorted_entity_id])
    # Iterate over target tables and perform update and insert operations

    query_collect_stats, query_collect_stats_extension = generate_collect_stats(sorted_entity_id, primary_index=primary_index,
                                                 partitioning=partitioning)

    feature_id_list = ','.join([str(x) for x in list(set(features_infos.FEATURE_ID.values))])
    for i, row in target_tables.iterrows():

        ENTITY_ID_WHERE_ = ' AND '.join([f'{row.iloc[0]}.{k}   = UPDATED_FEATURES.{k}' for k in sorted_entity_id])
        # SQL query to update existing feature values
        query_update = f"""
        {validtime_statement} 
        UPDATE {row.iloc[1]}.{row.iloc[0]}
        FROM (
            {validtime_statement2} 
            SELECT
                {ENTITY_ID_SELECT},
                NEW_FEATURES.FEATURE_ID,
                NEW_FEATURES.FEATURE_VALUE,
                NEW_FEATURES.FEATURE_VERSION
            FROM {_get_database_username()}.{volatile_table_name} NEW_FEATURES
            LEFT JOIN {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
            ON {ENTITY_ID_ON}
            AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
            WHERE 
            --({ENTITY_ID_WHERE_INS})
            --AND
             EXISTING_FEATURES.FEATURE_VERSION IS NOT NULL
             AND EXISTING_FEATURES.FEATURE_ID IN ({feature_id_list})
            AND NEW_FEATURES.FEATURE_DATABASE = '{row.iloc[1]}'
            AND NEW_FEATURES.FEATURE_TABLE = '{row.iloc[0]}'
        ) UPDATED_FEATURES
        SET
            FEATURE_VALUE = UPDATED_FEATURES.FEATURE_VALUE
        WHERE     {ENTITY_ID_WHERE_}
        AND {row.iloc[0]}.FEATURE_ID          = UPDATED_FEATURES.FEATURE_ID
            AND {row.iloc[0]}.FEATURE_VERSION = UPDATED_FEATURES.FEATURE_VERSION;
        """

        # SQL query to insert new feature values
        if validtime_statement == 'CURRENT VALIDTIME':
            query_insert = f"""
            {validtime_statement} 
            INSERT INTO {row.iloc[1]}.{row.iloc[0]} ({ENTITY_ID}, FEATURE_ID, FEATURE_VALUE, FEATURE_VERSION)
                SELECT
                    {ENTITY_ID_SELECT},
                    NEW_FEATURES.FEATURE_ID,
                    NEW_FEATURES.FEATURE_VALUE,
                    NEW_FEATURES.FEATURE_VERSION
                FROM {_get_database_username()}.{volatile_table_name} NEW_FEATURES
                LEFT JOIN {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
                ON 
                -- {ENTITY_ID_ON}
                --AND 
                EXISTING_FEATURES.FEATURE_VERSION IS NULL
                AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
                AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
                WHERE ({ENTITY_ID_WHERE_UP})
                AND NEW_FEATURES.FEATURE_DATABASE = '{row.iloc[1]}'
                AND NEW_FEATURES.FEATURE_TABLE = '{row.iloc[0]}'
            """
        elif tdfs4ds.FEATURE_STORE_TIME is not None:
            if tdfs4ds.END_PERIOD == 'UNTIL_CHANGED':
                end_period_ = '9999-01-01 00:00:00'
            else:
                end_period_ = tdfs4ds.END_PERIOD
            query_insert = f"""
            INSERT INTO {row.iloc[1]}.{row.iloc[0]} ({ENTITY_ID}, FEATURE_ID, FEATURE_VALUE, FEATURE_VERSION, ValidStart, ValidEnd)
                SELECT
                    {ENTITY_ID_SELECT},
                    NEW_FEATURES.FEATURE_ID,
                    NEW_FEATURES.FEATURE_VALUE,
                    NEW_FEATURES.FEATURE_VERSION,
                    TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}',
                    TIMESTAMP '{end_period_}'
                FROM {_get_database_username()}.{volatile_table_name} NEW_FEATURES
                LEFT JOIN {row.iloc[1]}.{row.iloc[0]} EXISTING_FEATURES
                ON {ENTITY_ID_ON}
                AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
                AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
                WHERE 
                --({ENTITY_ID_WHERE_UP})
                EXISTING_FEATURES.FEATURE_VERSION IS NULL
                AND NEW_FEATURES.FEATURE_DATABASE = '{row.iloc[1]}'
                AND NEW_FEATURES.FEATURE_TABLE = '{row.iloc[0]}'
            """

        entity_id_str = ', \n'.join([k for k in sorted_entity_id])

        if tdfs4ds.DISPLAY_LOGS: print(
            f'insert feature values of new {entity_id_str} combinations in {row.iloc[1]}.{row.iloc[0]}')
        if tdml.display.print_sqlmr_query:
            print(query_insert)
        execute_query(query_insert)
        if tdfs4ds.DISPLAY_LOGS: print(
            f'update feature values of existing {entity_id_str} combinations in {row.iloc[1]}.{row.iloc[0]}')
        if tdml.display.print_sqlmr_query:
            print(query_update)
        execute_query(query_update)
        # execute_query(query_collect_stats + f' ON {row.iloc[1]}.{row.iloc[0]}')
        # print(query_collect_stats + f' ON {row.iloc[1]}.{row.iloc[0]}')
        # if query_collect_stats_extension is not None:
        #     execute_query(query_collect_stats_extension + f' ON {row.iloc[1]}.{row.iloc[0]}')
        #     print(query_collect_stats_extension + f' ON {row.iloc[1]}.{row.iloc[0]}')

    return

def _store_feature_merge(entity_id, volatile_table_name, entity_null_substitute= {}, primary_index=None,
            partitioning='', features_infos = None, **kwargs):
    """
    Stores prepared feature data in specific feature tables within a Teradata database. This function performs updates and inserts
    on the feature tables based on the provided entity IDs and prepared feature data.

    Parameters:
    - entity_id (dict): A dictionary representing the entity ID, where keys are used to identify the entity.
    - prepared_features (tdml.DataFrame): A DataFrame containing the prepared feature data for ingestion.
    - **kwargs: Additional keyword arguments that can include:
        - schema (str): The schema name where the feature tables are located.
        - feature_catalog_name (str, optional): The name of the feature catalog table, defaulting to 'FS_FEATURE_CATALOG'.

    Returns:
    None: This function does not return any value but performs database operations.

    Note:
    - The function uses the Teradata temporal feature (VALIDTIME) for handling the valid time of the records.
    - It constructs SQL queries to update existing feature values and insert new ones based on the entity ID.
    - The function handles the entity ID, feature IDs, and versions for inserting and updating records.
    - It utilizes additional settings from the tdfs4ds module for configuring the feature store time and display logs.
    - This function assumes that the necessary database tables and schema are correctly set up and accessible.

    Example Usage:
    >>> entity_id_dict = {'customer_id': 'INTEGER'}
    >>> prepared_features = tdml.DataFrame(...)
    >>> store_feature(entity_id_dict, prepared_features)
    """

    # VALIDTIME handling
    if tdfs4ds.FEATURE_STORE_TIME is None:
        validtime_statement = 'CURRENT VALIDTIME'
        validtime_statement2 = validtime_statement
        validtime_start = 'CAST(CURRENT_TIME AS TIMESTAMP(0) WITH TIME ZONE)'
    else:
        validtime_statement = f"VALIDTIME PERIOD '({tdfs4ds.FEATURE_STORE_TIME},{tdfs4ds.END_PERIOD})'"
        validtime_statement2 = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"
        validtime_start = f"CAST('{tdfs4ds.FEATURE_STORE_TIME}' AS TIMESTAMP(0) WITH TIME ZONE)"

    end_period_ = '9999-01-01 00:00:00' if tdfs4ds.END_PERIOD == 'UNTIL_CHANGED' else tdfs4ds.END_PERIOD

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "FEATURE_STORE_TIME=%s | END_PERIOD=%s", tdfs4ds.FEATURE_STORE_TIME, tdfs4ds.END_PERIOD)
        logger_safe("debug", "entity_id=%s", entity_id)

    # Entity id helpers
    sorted_entity_id = sorted(list(entity_id.keys()))
    ENTITY_ID = ','.join(sorted_entity_id)

    # Count rows in volatile table
    count_features = pd.DataFrame(
        tdml.execute_sql(
            f"""
            SEL count(*) as NB_ROWS
            FROM {_get_database_username()}.{volatile_table_name}
            """
        ).fetchall(),
        columns=['NB_ROWS']
    )

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "count_features=%s", count_features)
        logger_safe("debug", "features_infos initial=%s", features_infos)

    if count_features.shape[0] > 0:
        features_infos['NB_ROWS'] = count_features['NB_ROWS'].values[0]
    else:
        features_infos['NB_ROWS'] = 0

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "features_infos updated=%s", features_infos)

    # Compute target tables
    target_tables = features_infos[['FEATURE_TABLE', 'FEATURE_DATABASE', 'NB_ROWS']].groupby(
        ['FEATURE_TABLE', 'FEATURE_DATABASE']
    ).sum().reset_index()

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "target_tables=%s", target_tables)

    # Optional display (keep existing UX semantics)
    if getattr(tdfs4ds, "DISPLAY_LOGS", False):
        try:
            display_table(target_tables[['FEATURE_DATABASE', 'FEATURE_TABLE', 'NB_ROWS']])
        except Exception as e:
            logger_safe("warning", "display_table failed: %s", str(e).split('\n')[0])

    ENTITY_ID_ON = ' AND '.join([f'NEW_FEATURES.{k} = EXISTING_FEATURES.{k}' for k in sorted_entity_id])
    ENTITY_ID_SELECT = ', \n'.join(['NEW_FEATURES.' + k for k in sorted_entity_id])

    queries = []
    for _, row in features_infos.iterrows():
        features_infos_ = features_infos[
            (features_infos.FEATURE_TABLE == row['FEATURE_TABLE']) &
            (features_infos.FEATURE_DATABASE == row['FEATURE_DATABASE'])
        ]
        feature_id_list = ','.join([str(x) for x in sorted(set(features_infos_.FEATURE_ID.values))])
        feature_version_list = ','.join(["'" + x + "'" for x in sorted(set(features_infos_.FEATURE_VERSION.values))])

        # Build nested query
        nested_query = f"""
            SEL 
                {ENTITY_ID}
              , {row['FEATURE_ID']} AS FEATURE_ID
              , {row['FEATURE_NAME']} AS FEATURE_VALUE
              , '{row['FEATURE_VERSION']}' AS FEATURE_VERSION
            FROM {_get_database_username()}.{volatile_table_name}
        """

        if tdfs4ds.FEATURE_STORE_TIME is None:
            query_merge = f"""
            {validtime_statement}
            MERGE INTO {row['FEATURE_DATABASE']}.{row['FEATURE_TABLE']} EXISTING_FEATURES
            USING ( {nested_query} ) NEW_FEATURES
            ON {ENTITY_ID_ON}
            AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
            AND NEW_FEATURES.FEATURE_ID IN ({feature_id_list})
            AND EXISTING_FEATURES.FEATURE_ID IN ({feature_id_list})
            AND EXISTING_FEATURES.FEATURE_VERSION IN ({feature_version_list})
            WHEN MATCHED THEN
                UPDATE SET FEATURE_VALUE = NEW_FEATURES.FEATURE_VALUE
            WHEN NOT MATCHED THEN
                INSERT
                (
                    {ENTITY_ID_SELECT},
                    NEW_FEATURES.FEATURE_ID,
                    NEW_FEATURES.FEATURE_VALUE,
                    NEW_FEATURES.FEATURE_VERSION
                )
            """
        else:
            query_merge = f"""
            {validtime_statement}
            MERGE INTO {row['FEATURE_DATABASE']}.{row['FEATURE_TABLE']} EXISTING_FEATURES
            USING ( {nested_query} ) NEW_FEATURES
            ON {ENTITY_ID_ON}
            AND NEW_FEATURES.FEATURE_ID = EXISTING_FEATURES.FEATURE_ID
            AND NEW_FEATURES.FEATURE_VERSION = EXISTING_FEATURES.FEATURE_VERSION
            AND EXISTING_FEATURES.FEATURE_ID IN ({feature_id_list})
            AND NEW_FEATURES.FEATURE_ID IN ({feature_id_list})
            AND EXISTING_FEATURES.FEATURE_VERSION IN ({feature_version_list})
            WHEN MATCHED THEN
                UPDATE SET FEATURE_VALUE = NEW_FEATURES.FEATURE_VALUE
            WHEN NOT MATCHED THEN
                INSERT
                (
                    {ENTITY_ID_SELECT},
                    NEW_FEATURES.FEATURE_ID,
                    NEW_FEATURES.FEATURE_VALUE,
                    NEW_FEATURES.FEATURE_VERSION,
                    {validtime_start},
                    '{end_period_}'
                )
            """

        if getattr(tdfs4ds, "DEBUG_MODE", False):
            entity_id_str = ', '.join(sorted_entity_id)
            logger_safe(
                "debug",
                "Merging feature values for entity keys (%s) into %s.%s",
                entity_id_str, row['FEATURE_DATABASE'], row['FEATURE_TABLE']
            )
            logger_safe("debug", "Query (truncated): %s", "\n".join(query_merge.splitlines()[:12]) + "\n...")

        queries.append(query_merge)

    try:
        start_time = time.time()

        for q in queries:
            if getattr(tdfs4ds, "DEBUG_MODE", False):
                logger_safe("debug", "Executing merge (head): %s", "\n".join(q.split('\n')[0:3]))
            execute_query(q)

        elapsed_time = time.time() - start_time
        formatted_elapsed_time = seconds_to_dhms(elapsed_time)
        logger_safe(
            "info",
            "Storage of prepared features (merge-only) completed in %s (%.3fs)",
            formatted_elapsed_time, elapsed_time
        )
    except Exception as e:
        logger_safe("exception", "Feature storage (merge) failed: %s", str(e).split('\n')[0])
        raise

    return

def store_feature(entity_id, volatile_table_name, entity_null_substitute = {},primary_index=None,
            partitioning='', features_infos = None, **kwargs):
    """
    Conditionally stores prepared feature data in specific feature tables within a Teradata database. This function decides
    whether to perform updates and inserts on the feature tables based on a global configuration.

    Parameters:
    - entity_id (dict): A dictionary representing the entity ID, where keys are used to identify the entity.
    - prepared_features (tdml.DataFrame): A DataFrame containing the prepared feature data for ingestion.
    - **kwargs: Additional keyword arguments for further customization and configurations.

    Returns:
    None: This function does not return any value but performs database operations based on the specified condition.

    Example Usage:
    >>> entity_id_dict = {'customer_id': 'INTEGER'}
    >>> prepared_features = tdml.DataFrame(...)
    >>> store_feature(entity_id_dict, prepared_features)
    """

    start_time = time.time()

    # Choose storage strategy
    if tdfs4ds.STORE_FEATURE == 'UPDATE_INSERT':
        logger_safe("info", "Storing features using UPDATE/INSERT strategy.")
        _store_feature_update_insert(
            entity_id,
            volatile_table_name,
            entity_null_substitute=entity_null_substitute,
            primary_index=primary_index,
            partitioning=partitioning,
            features_infos=features_infos,
            **kwargs
        )
    elif tdfs4ds.STORE_FEATURE == 'MERGE':
        logger_safe("info", "Storing features using MERGE strategy.")
        _store_feature_merge(
            entity_id,
            volatile_table_name,
            entity_null_substitute=entity_null_substitute,
            primary_index=primary_index,
            partitioning=partitioning,
            features_infos=features_infos,
            **kwargs
        )
    else:
        logger_safe(
            "warning",
            "Unknown STORE_FEATURE strategy '%s'. No storage operation was performed.",
            tdfs4ds.STORE_FEATURE
        )

    # Log duration
    elapsed_time = time.time() - start_time
    formatted_elapsed_time = seconds_to_dhms(elapsed_time)
    logger_safe(
        "info",
        "Storage of prepared features completed in %s (%.3fs)",
        formatted_elapsed_time,
        elapsed_time
    )

def prepare_feature_ingestion_tdstone2(df, entity_id):
    """
    Prepares a DataFrame for feature ingestion into a tdstone2 feature store by transforming the data structure.
    This function unpivots the DataFrame and adds necessary columns for entity IDs, feature names, feature values,
    and a predefined feature version. It creates a volatile table in the database to facilitate this transformation.

    Parameters:
    - df (tdml.DataFrame): The input DataFrame containing the feature data. The DataFrame should be structured
      in a way that is compatible with tdstone2 feature store requirements.
    - entity_id (list/dict/other): A representation of the entity ID. If a dictionary, the keys are used as entity IDs.
                                   If a list or another data type, it is used directly as the entity ID.

    Returns:
    - tdml.DataFrame: A transformed DataFrame suitable for feature store ingestion.
    - str: The name of the volatile table created in the database for storing the transformed data.

    Note:
    - The function requires that the input DataFrame 'df' has a valid table name and is compatible with tdml operations.
    - It automatically handles the creation and management of a volatile table in the database.
    - 'ID_PROCESS' is used as the default feature version identifier.
    - The transformed DataFrame includes columns for each entity ID, 'FEATURE_NAME', 'FEATURE_VALUE', and 'FEATURE_VERSION'.

    Example Usage:
    >>> input_df = tdml.DataFrame(...)
    >>> entity_id_dict = {'customer_id': 'INTEGER'}
    >>> transformed_df, table_name = prepare_feature_ingestion_tdstone2(input_df, entity_id_dict)
    """

    # Ensure the internal table name of the DataFrame is set, necessary for further processing.
    df._DataFrame__execute_node_and_set_table_name(df._nodeid, df._metaexpr)

    if type(entity_id) == list:
        list_entity_id = entity_id
    elif type(entity_id) == dict:
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Combine entity ID columns with feature name and value columns to form the output column list.
    output_columns = ', \n'.join(list_entity_id + ['FEATURE_NAME', 'FEATURE_VALUE'])
    primary_index = ','.join(list_entity_id)

    # Define a query segment to assign feature versions.
    version_query = "ID_PROCESS AS FEATURE_VERSION"

    # Create a volatile table name based on the original table's name, ensuring it is unique.
    if tdfs4ds.USE_VOLATILE_TABLE:
        volatile_table_name = df._table_name.split('.')[1].replace('"', '')
        volatile_table_name = f'temp_{volatile_table_name}'
        volatile_verb = 'VOLATILE'
        volatile_expression = 'ON COMMIT PRESERVE ROWS'
    else:
        volatile_table_name = df._table_name.split('.')[1].replace('"', '')
        volatile_table_name = f'"{tdfs4ds.SCHEMA}"."temp_{volatile_table_name}"'
        volatile_verb = ''
        volatile_expression = ''

    # Construct the SQL query to create the volatile table with the transformed data.
    query = f"""
    CREATE {volatile_verb} TABLE {volatile_table_name} AS
    (
    SELECT 
    {output_columns},
    {version_query}
    FROM {df._table_name}
    ) WITH DATA
    PRIMARY INDEX ({primary_index})
    {volatile_expression}
    """
    # Execute the SQL query to create the volatile table.
    try:
        tdml.execute_sql(query)
    except Exception as e:
        if tdfs4ds.DISPLAY_LOGS:
            print(str(e).split('\n')[0])
        tdml.execute_sql(f'DELETE {volatile_table_name}')

    # Optionally print the query if the display flag is set.
    if tdml.display.print_sqlmr_query:
        print(query)

    # Return the DataFrame representation of the volatile table and its name.
    if tdfs4ds.USE_VOLATILE_TABLE:
        return tdml.DataFrame(tdml.in_schema(_get_database_username(), volatile_table_name)), volatile_table_name
    else:
        return tdml.DataFrame(volatile_table_name), volatile_table_name


