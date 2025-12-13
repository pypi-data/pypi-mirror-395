__version__ = '0.2.4.46'
import logging
import json

# Setup the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format to include timestamp
    datefmt='%Y-%m-%d %H:%M:%S'  # Set the date/time format
)

# Helper: central logging gate controlled by tdfs4ds.DISPLAY_LOGS
def logger_safe(level, message, *args, **kwargs):
    """
    Wrapper around the global `logger` that only emits logs when
    tdfs4ds.DISPLAY_LOGS is True. `level` is a string like "info", "error", etc.
    """
    if getattr(tdfs4ds, "DISPLAY_LOGS", True):
        getattr(logger, level)(message, *args, **kwargs)

logger = logging.getLogger(__name__)

from tdfs4ds.feature_store.feature_query_retrieval import get_available_entity_id_records, write_where_clause_filter
from tdfs4ds.process_store.process_followup import follow_up_report
from tdfs4ds.dataset.dataset_catalog import DatasetCatalog, Dataset

DATA_DOMAIN             = None
SCHEMA                  = None
FEATURE_CATALOG_NAME         = 'FS_FEATURE_CATALOG'
FEATURE_CATALOG_NAME_VIEW    = 'FS_V_FEATURE_CATALOG'
PROCESS_CATALOG_NAME         = 'FS_PROCESS_CATALOG'
PROCESS_CATALOG_NAME_VIEW    = 'FS_V_PROCESS_CATALOG'
PROCESS_CATALOG_NAME_VIEW_FEATURE_SPLIT    = 'FS_V_PROCESS_CATALOG_FEATURE_SPLIT'
DATASET_CATALOG_NAME         = 'FS_DATASET'

DATA_DISTRIBUTION_NAME  = 'FS_DATA_DISTRIBUTION'
FOLLOW_UP_NAME          = 'FS_FOLLOW_UP'
DATA_DISTRIBUTION_TEMPORAL = False
FILTER_MANAGER_NAME     = 'FS_FILTER_MANAGER'

END_PERIOD              = 'UNTIL_CHANGED' #'9999-01-01 00:00:00+00:00'
FEATURE_STORE_TIME      = None #'9999-01-01 00:00:00+00:00'
FEATURE_VERSION_DEFAULT = 'dev.0.0'
DISPLAY_LOGS            = True
DEBUG_MODE              = False

USE_VOLATILE_TABLE      = True
STORE_FEATURE           = 'MERGE' #'UPDATE_INSERT'
REGISTER_FEATURE        = 'MERGE' #'UPDATE_INSERT'
REGISTER_PROCESS        = 'MERGE' #'UPDATE_INSERT'
BUILD_DATASET_AT_UPLOAD = False

FEATURE_PARTITION_N     = 20000
FEATURE_PARTITION_EACH  = 1

VARCHAR_SIZE            = 1024

import warnings
warnings.filterwarnings('ignore')

import teradataml as tdml
from tdfs4ds.utils.lineage import crystallize_view
from tdfs4ds.utils.filter_management import FilterManager
from tdfs4ds.utils.info import seconds_to_dhms
import tdfs4ds.feature_store
import tdfs4ds.process_store
import tdfs4ds.datasets
import time

import inspect
from tqdm.auto import tqdm  # auto picks the right frontend (notebook/terminal)

from tdfs4ds.feature_store.feature_data_processing import generate_on_clause

import uuid

# Generate a UUID
RUN_ID       = str(uuid.uuid4())
PROCESS_TYPE = 'RUN PROCESS'

try:
    SCHEMA = tdml.context.context._get_current_databasename()
    if SCHEMA is None:
        logger.warning("No default database detected for feature store.")
        logger.warning('Please set it explicitly: tdfs4ds.feature_store.schema = "<feature store database>"')
    else:
        logger.info("Default database detected for feature store: %s", SCHEMA)
        logger.info('tdfs4ds.feature_store.schema = "%s"', SCHEMA)

        if DATA_DOMAIN is None:
            DATA_DOMAIN = SCHEMA
            logger.info("DATA_DOMAIN not set. Defaulting to SCHEMA: %s", DATA_DOMAIN)
            logger.info('You can override it using: tdfs4ds.DATA_DOMAIN = "<your data domain>"')

except Exception as e:
    logger.error("Could not determine current database: %s", str(e).split('\n')[0])
    logger.warning("Please specify the feature store database manually:")
    logger.warning('tdfs4ds.feature_store.schema = "<feature store database>"')


def setup(database, if_exists='fail'):
    """
    Initialize the feature store environment by creating catalog tables and views.
    """

    from tdfs4ds.feature_store.feature_store_management import feature_store_catalog_creation
    from tdfs4ds.process_store.process_store_catalog_management import process_store_catalog_creation

    tdfs4ds.SCHEMA = database
    logger_safe("info", "Setting up feature store in database: %s", database)

    if if_exists == 'replace':
        logger_safe("info", "Replacing existing catalog tables if they exist.")
        for table in [tdfs4ds.FEATURE_CATALOG_NAME, tdfs4ds.PROCESS_CATALOG_NAME, tdfs4ds.DATA_DISTRIBUTION_NAME]:
            try:
                tdml.db_drop_table(table_name=table, schema_name=database)
                logger_safe("info", "Dropped table %s.%s", database, table)
            except Exception as e:
                logger_safe("warning", "Could not drop table %s.%s: %s", database, table, str(e).split('\n')[0])

        DatasetCatalog(schema_name=database, name=tdfs4ds.DATASET_CATALOG_NAME).drop_catalog()

    try:
        tdfs4ds.FEATURE_CATALOG_NAME = feature_store_catalog_creation()
        logger_safe("info", "Feature catalog table created: %s in database %s", tdfs4ds.FEATURE_CATALOG_NAME, database)
    except Exception as e:
        logger_safe("error", "Feature catalog creation failed: %s", str(e).split('\n')[0])

    try:
        (tdfs4ds.PROCESS_CATALOG_NAME,
         tdfs4ds.DATA_DISTRIBUTION_NAME,
         tdfs4ds.FILTER_MANAGER_NAME) = process_store_catalog_creation()

        logger_safe("info", "Process catalog table created: %s", tdfs4ds.PROCESS_CATALOG_NAME)
        logger_safe("info", "Data distribution table created: %s", tdfs4ds.DATA_DISTRIBUTION_NAME)
        logger_safe("info", "Filter manager table created: %s", tdfs4ds.FILTER_MANAGER_NAME)
    except Exception as e:
        logger_safe("error", "Process catalog creation failed: %s", str(e).split('\n')[0])

    try:
        tdfs4ds.process_store.process_followup.follow_up_table_creation()
        logger_safe("info", "Follow-up table created successfully.")
    except Exception as e:
        logger_safe("error", "Follow-up table creation failed: %s", str(e).split('\n')[0])

    tdfs4ds.feature_store.feature_store_management.feature_store_catalog_view_creation()
    tdfs4ds.process_store.process_store_catalog_management.process_store_catalog_view_creation()

    dataset_catalog = DatasetCatalog(schema_name=database, name=tdfs4ds.DATASET_CATALOG_NAME)
    if not dataset_catalog._exists():
        dataset_catalog.create_catalog()
        logger_safe("info", "Dataset catalog created: %s", tdfs4ds.DATASET_CATALOG_NAME)

    logger_safe("info", "Setup complete.")
    return


def connect(
    database                  = tdfs4ds.SCHEMA,
    feature_catalog_name      = tdfs4ds.FEATURE_CATALOG_NAME,
    process_catalog_name      = tdfs4ds.PROCESS_CATALOG_NAME,
    data_distribution_name    = tdfs4ds.DATA_DISTRIBUTION_NAME,
    filter_manager_name       = tdfs4ds.FILTER_MANAGER_NAME,
    followup_name             = tdfs4ds.FOLLOW_UP_NAME,
    feature_catalog_name_view = tdfs4ds.FEATURE_CATALOG_NAME_VIEW,
    process_catalog_name_view = tdfs4ds.PROCESS_CATALOG_NAME_VIEW,
    dataset_catalog_name      = tdfs4ds.DATASET_CATALOG_NAME,
    create_if_missing         = False
):
    if database is None:
        raise ValueError("database parameter is None.")
    tdfs4ds.SCHEMA = database
    logger_safe("info", "Connecting to feature store in database: %s", database)

    tables = [x.lower() for x in list(tdml.db_list_tables(schema_name=tdfs4ds.SCHEMA, object_type='table').TableName.values)]

    feature_exists = feature_catalog_name.lower() in tables
    process_exists = process_catalog_name.lower() in tables
    distrib_exists = data_distribution_name.lower() in tables
    filter_manager_exists = filter_manager_name.lower() in tables
    followup_name_exists = followup_name.lower() in tables

    if not (feature_exists and process_exists and distrib_exists and filter_manager_exists):
        if not create_if_missing:
            logger_safe("warning", "Feature store components missing and create_if_missing=False")
            return False
        logger_safe("info", "Missing components detected; creating missing parts...")
        if not feature_exists:
            tdfs4ds.feature_store.feature_store_management.feature_store_catalog_creation()
        if not process_exists:
            tdfs4ds.process_store.process_store_catalog_management.process_store_catalog_creation()
        if not distrib_exists:
            tdfs4ds.data_distribution.data_distribution_catalog_creation()
        if not filter_manager_exists:
            tdfs4ds.filter_manager.filter_manager_catalog_creation()

    if not followup_name_exists:
        logger_safe("info", "Creating follow-up table: %s", followup_name)
        tdfs4ds.process_store.process_followup.follow_up_table_creation()
    tdfs4ds.FOLLOW_UP_NAME = followup_name

    # Set catalog names
    tdfs4ds.FEATURE_CATALOG_NAME = feature_catalog_name
    tdfs4ds.PROCESS_CATALOG_NAME = process_catalog_name
    tdfs4ds.DATA_DISTRIBUTION_NAME = data_distribution_name
    tdfs4ds.FILTER_MANAGER_NAME = filter_manager_name
    tdfs4ds.PROCESS_CATALOG_NAME_VIEW = process_catalog_name_view
    tdfs4ds.FEATURE_CATALOG_NAME_VIEW = feature_catalog_name_view

    process_list = tdml.DataFrame(tdml.in_schema(database, process_catalog_name))
    if 'ENTITY_NULL_SUBSTITUTE' not in process_list.columns:
        logger_safe("warning", "ENTITY_NULL_SUBSTITUTE column missing. Upgrading catalog.")
        tdfs4ds.process_store.process_store_catalog_management.upgrade_process_catalog()

    tdfs4ds.feature_store.feature_store_management.feature_store_catalog_view_creation()
    tdfs4ds.process_store.process_store_catalog_management.process_store_catalog_view_creation()

    # Dataset Catalog
    tdfs4ds.DATASET_CATALOG_NAME = dataset_catalog_name
    dataset_catalog = DatasetCatalog(schema_name=database, name=dataset_catalog_name)
    if not dataset_catalog._exists():
        dataset_catalog.create_catalog()
        logger_safe("info", "Dataset catalog created: %s", dataset_catalog_name)

    # Detect temporal distribution
    def is_data_distribution_temporal():
        return 'PERIOD' in tdfs4ds.utils.lineage.get_ddl(
            view_name=tdfs4ds.DATA_DISTRIBUTION_NAME,
            schema_name=tdfs4ds.SCHEMA,
            object_type='table'
        )

    tdfs4ds.DATA_DISTRIBUTION_TEMPORAL = is_data_distribution_temporal()
    logger_safe("info", "Connected to feature store successfully.")
    return True




def feature_catalog():
    """
    Retrieve a list of all features available in the feature store.

    This function queries the feature store to obtain a comprehensive list of features
    that have been defined and stored. It leverages the feature store's query retrieval
    functionality to compile and return this list. This can be useful for understanding
    what features are available for analysis, machine learning models, or other purposes
    within the data ecosystem.

    Returns:
    - list: A list of features available in the feature store as a teradata dataframe at
            the tdfs4ds.FEATURE_STORE_TIME valid time.
    """
    return tdfs4ds.feature_store.feature_query_retrieval.list_features()


def process_catalog():
    """
    Retrieve a list of all processes registered in the process store.

    This function performs a query against the process store to gather a list of all
    processes that have been registered and are administrable. It utilizes the process
    store's process query administration capabilities to fetch and return this list.
    This is useful for users looking to get an overview of the data processing workflows,
    transformations, and other processes that have been established within the data
    infrastructure.

    Returns:
    - list: A list of processes registered in the process store as a teradata dataframe at
            the tdfs4ds.FEATURE_STORE_TIME valid time.
    """
    return tdfs4ds.process_store.process_query_administration.list_processes()

def dataset_catalog():
    """
    Retrieve a list of all datasets registered in the dataset store.

    This function performs a query against the dataset store to gather a list of all
    datasets that have been registered and are administrable. 

    """
    return DatasetCatalog(schema_name=tdfs4ds.SCHEMA, name=tdfs4ds.DATASET_CATALOG_NAME).catalog

def get_dataset_entity(dataset_id = None):
    return DatasetCatalog(schema_name=tdfs4ds.SCHEMA, name=tdfs4ds.DATASET_CATALOG_NAME).get_dataset_entity(dataset_id)

def get_dataset_features(dataset_id = None):
    return DatasetCatalog(schema_name=tdfs4ds.SCHEMA, name=tdfs4ds.DATASET_CATALOG_NAME).get_dataset_features(dataset_id)

def run(process_id, return_dataset=False, force_compute=False, force_varchar_length=None):
    """
    Executes a specific process from the feature store identified by the process ID.
    Uses global `logger` for diagnostics (gated by tdfs4ds.DISPLAY_LOGS).
    """

    if tdfs4ds.PROCESS_TYPE is None:
        PROCESS_TYPE_ = 'RUN PROCESS'
        tdfs4ds.RUN_ID = str(uuid.uuid4())
    else:
        PROCESS_TYPE_ = tdfs4ds.PROCESS_TYPE

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe("debug", "def run | tdfs4ds.FEATURE_STORE_TIME=%s", tdfs4ds.FEATURE_STORE_TIME)

    if tdfs4ds.FEATURE_STORE_TIME is None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"

    # Construct SQL query to retrieve process details by process ID
    query = f"""
    SELECT *
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW} A
    WHERE A.PROCESS_ID = '{process_id}'
    """

    logger_safe(
        "info",
        "Starting run | run_id=%s | process_type=%s | process_id=%s | return_dataset=%s | force_compute=%s | force_varchar_length=%s",
        tdfs4ds.RUN_ID, PROCESS_TYPE_, process_id, return_dataset, force_compute, force_varchar_length
    )

    # Executing the query and converting the result to Pandas DataFrame
    df = tdml.DataFrame.from_query(query).to_pandas()

    # Check if exactly one record is returned, else log an error and return
    if df.shape[0] != 1:
        logger_safe(
            "error",
            "Process catalog lookup returned %s record(s); expected 1. Check table %s.%s. Query: %s",
            df.shape[0], tdfs4ds.SCHEMA, tdfs4ds.PROCESS_CATALOG_NAME_VIEW, query.strip()
        )
        return

    # Fetching the filter manager
    filter_schema_name = df['FILTER_DATABASE_NAME'].values[0]
    if filter_schema_name is None:
        filtermanager = None
    else:
        filter_view_name = df['FILTER_VIEW_NAME'].values[0]
        filter_table_name = df['FILTER_TABLE_NAME'].values[0]  # kept for parity; not used directly here
        filtermanager = FilterManager(table_name=filter_view_name, schema_name=filter_schema_name)

    # Fetching process metadata
    process_type   = df['PROCESS_TYPE'].values[0]
    primary_index  = df['FOR_PRIMARY_INDEX'].values[0]
    if primary_index is not None:
        primary_index = [x.strip() for x in primary_index.split(',') if x.strip()]
    partitioning   = df['FOR_DATA_PARTITIONING'].values[0]
    DATA_DOMAIN    = df['DATA_DOMAIN'].values[0]

    logger_safe(
        "info",
        "Process metadata | process_id=%s | process_type=%s | primary_index=%s | partitioning=%s | data_domain=%s | validtime=%s",
        process_id, process_type, primary_index, partitioning, DATA_DOMAIN, validtime_statement
    )

    # Handling 'denormalized view' process type
    if process_type == 'denormalized view':
        view_name              = df['VIEW_NAME'].values[0]
        entity_id              = [x.strip() for x in df['ENTITY_ID'].values[0].split(',') if x.strip()]
        entity_null_substitute = eval(df['ENTITY_NULL_SUBSTITUTE'].values[0])
        feature_names          = [x.strip() for x in df['FEATURE_NAMES'].values[0].split(',') if x.strip()]

        df_data = tdml.DataFrame(tdml.in_schema(view_name.split('.')[0], view_name.split('.')[1]))

        if getattr(tdfs4ds, "DEBUG_MODE", False):
            logger_safe("debug", "run | entity_id=%s", entity_id)
            logger_safe("debug", "run | entity_null_substitute=%s", entity_null_substitute)
            logger_safe("debug", "run | feature_names=%s", feature_names)
            logger_safe("debug", "run | process_id=%s", process_id)
            logger_safe("debug", "run | primary_index=%s", primary_index)
            logger_safe("debug", "run | partitioning=%s", partitioning)

        dataset = _upload_features(
            df_data,
            entity_id,
            feature_names,
            feature_versions=process_id,
            primary_index=primary_index,
            partitioning=partitioning,
            filtermanager=filtermanager,
            entity_null_substitute=entity_null_substitute,
            process_id=process_id,
            force_compute=force_compute,
            force_varchar_length=force_varchar_length
        )

    # Handling 'tdstone2 view' process type
    elif process_type == 'tdstone2 view':
        logger_safe("warning", "Process type 'tdstone2 view' not implemented yet for process_id=%s", process_id)
        dataset = None

    else:
        logger_safe("error", "Unknown process type '%s' for process_id=%s", process_type, process_id)
        dataset = None

    if return_dataset:
        logger_safe("info", "Run finished with dataset | run_id=%s | process_id=%s", tdfs4ds.RUN_ID, process_id)
        return dataset
    else:
        logger_safe("info", "Run finished without dataset | run_id=%s | process_id=%s", tdfs4ds.RUN_ID, process_id)
        return


def upload_features(
    df,
    entity_id,
    feature_names,
    metadata={},
    primary_index=None,
    partitioning='',
    filtermanager=None,
    entity_null_substitute={},
    force_compute=True,
    force_varchar_length=1024
):
    """
    Uploads feature data from a DataFrame to the feature store for a specified entity.
    All diagnostics go through `logger_safe()` which respects `tdfs4ds.DISPLAY_LOGS`.
    """

    from tdfs4ds.utils.info import get_column_types
    from tdfs4ds.utils.query_management import execute_query
    from tdfs4ds.process_store.process_registration_management import register_process_view

    # Convert entity_id to a dictionary if it's not already one
    if isinstance(entity_id, list):
        entity_id.sort()
        entity_id = get_column_types(df, entity_id)
        logger_safe("debug", "entity_id converted to dict: %s", entity_id)

    elif isinstance(entity_id, str):
        entity_id = [entity_id]
        entity_id = get_column_types(df, entity_id)
        logger_safe("debug", "entity_id converted to dict: %s", entity_id)

    # Normalize feature_names
    if not isinstance(feature_names, list):
        logger_safe("debug", "feature_names is not a list: %s", feature_names)
        if isinstance(feature_names, str) and ',' in feature_names:
            feature_names = [x.strip() for x in feature_names.split(',')]
        else:
            feature_names = [feature_names]
        logger_safe("debug", "feature_names converted to list: %s", feature_names)
        logger_safe("debug", "Check the conversion is as expected.")

    # Normalize primary_index
    if primary_index is not None and not isinstance(primary_index, list):
        logger_safe("debug", "primary_index is not a list: %s", primary_index)
        if isinstance(primary_index, str) and ',' in primary_index:
            primary_index = [x.strip() for x in primary_index.split(',')]
        else:
            primary_index = [primary_index]
        logger_safe("debug", "primary_index converted to list: %s", primary_index)
        logger_safe("debug", "Check the conversion is as expected.")

    # Partitioning
    partitioning = tdfs4ds.utils.info.generate_partitioning_clause(partitioning=partitioning)

    logger_safe("debug", "filtermanager: %s", filtermanager)

    # Register process -> get SQL(s) + process_id
    query_insert, process_id, query_insert_dist, query_insert_filtermanager = register_process_view.__wrapped__(
        view_name       = df,
        entity_id       = entity_id,
        feature_names   = feature_names,
        metadata        = metadata,
        with_process_id = True,
        primary_index   = primary_index,
        partitioning    = partitioning,
        filtermanager   = filtermanager,
        entity_null_substitute = entity_null_substitute
    )

    logger_safe("info", "Registered process (process_id=%s) for upload_features", process_id)

    # Execute queries
    try:
        execute_query(query_insert)
        logger_safe("info", "Executed main insert query for process_id=%s", process_id)
    except Exception as e:
        logger_safe("exception", "Main insert query failed for process_id=%s", process_id)
        raise

    try:
        execute_query(query_insert_dist)
        logger_safe("info", "Executed distribution insert query for process_id=%s", process_id)
    except Exception as e:
        logger_safe("exception", "Distribution insert query failed for process_id=%s", process_id)
        raise

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        # Avoid dumping entire SQL in normal logs; keep it debug-only.
        logger_safe("debug", "query_insert_filtermanager: %s", query_insert_filtermanager)

    if query_insert_filtermanager is not None:
        try:
            execute_query(query_insert_filtermanager)
            logger_safe("info", "Executed filtermanager insert query for process_id=%s", process_id)
        except Exception as e:
            logger_safe("exception", "Filtermanager insert query failed for process_id=%s", process_id)
            raise

    # Run the registered process (with/without dataset)
    PROCESS_TYPE = tdfs4ds.PROCESS_TYPE
    tdfs4ds.PROCESS_TYPE = 'UPLOAD_FEATURES'
    if getattr(tdfs4ds, "BUILD_DATASET_AT_UPLOAD", False):
        tdfs4ds.PROCESS_TYPE = 'UPLOAD_FEATURES WITH DATASET VALIDATION'
    tdfs4ds.RUN_ID = str(uuid.uuid4())

    logger_safe(
        "info",
        "Starting run (run_id=%s, process_type=%s, process_id=%s, force_compute=%s, force_varchar_length=%s)",
        tdfs4ds.RUN_ID, tdfs4ds.PROCESS_TYPE, process_id, force_compute, force_varchar_length
    )

    try:
        if getattr(tdfs4ds, "BUILD_DATASET_AT_UPLOAD", False):
            dataset = run(
                process_id=process_id,
                return_dataset=True,
                force_compute=force_compute,
                force_varchar_length=force_varchar_length
            )
            logger_safe("info", "Run completed with dataset (run_id=%s, process_id=%s)", tdfs4ds.RUN_ID, process_id)
            return dataset
        else:
            run(
                process_id=process_id,
                return_dataset=False,
                force_compute=force_compute,
                force_varchar_length=force_varchar_length
            )
            logger_safe("info", "Run completed without dataset (run_id=%s, process_id=%s)", tdfs4ds.RUN_ID, process_id)
            return

    except Exception as e:
        # Keep your existing follow-up close behavior, but ensure the error is logged.
        try:
            tdfs4ds.process_store.process_followup.followup_close(
                run_id       = tdfs4ds.RUN_ID,
                process_type = tdfs4ds.PROCESS_TYPE,
                process_id   = process_id,
                status       = 'FAILED,' + str(e).split('\n')[0]
            )
        finally:
            logger_safe("exception", "Run failed (run_id=%s, process_id=%s): %s",
                tdfs4ds.RUN_ID, process_id, str(e).split('\n')[0]
            )
        raise
    finally:
        # Restore previous process type just in case the caller relies on it.
        tdfs4ds.PROCESS_TYPE = PROCESS_TYPE



def _upload_features(
    df, entity_id, feature_names,
    feature_versions=FEATURE_VERSION_DEFAULT,
    primary_index=None, partitioning='',
    filtermanager=None, entity_null_substitute={},
    process_id=None, force_compute=False,
    force_varchar_length=None
):
    """
    Uploads a set of features into the Feature Store for a given entity.

    This function registers an entity and its associated features in the feature catalog
    if they are not already defined, prepares the data for ingestion, and stores it in the
    feature store. It also supports incremental feature computation and conditional execution
    depending on prior runs.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe containing entity keys and feature columns to upload.
    entity_id : str, list, or dict
        Identifier(s) for the entity. Can be:
            - A string (single entity key)
            - A list of key column names
            - A dict mapping column names to data types
        If not a dict, entity metadata is inferred automatically.
    feature_names : list of str
        List of feature column names to upload from `df`.
    feature_versions : dict or int, optional
        Feature version(s). If a single integer is provided, it is applied to all features.
        If a dict is provided, it maps each feature name to its version.
        Default is FEATURE_VERSION_DEFAULT.
    primary_index : str or list, optional
        Primary index to use when storing features in Teradata.
    partitioning : str, optional
        Partitioning clause for feature store tables. Default is ''.
    filtermanager : FilterManager, optional
        If provided, features are built iteratively per filter step.
    entity_null_substitute : dict, optional
        Replacement values for nulls in entity keys.
        Example: {'customer_id': -1}
    process_id : str, optional
        Identifier for the process execution, used for follow-up logging.
    force_compute : bool, optional
        If True, forces recomputation even if the same process_id and timestamp were
        already computed earlier. If False, the computation is skipped when existing
        results are detected. Default is False.
    force_varchar_length : int, optional
        If provided, all VARCHAR feature columns are resized to this length
        before ingestion.

    Returns
    -------
    pandas.DataFrame or None
        If BUILD_DATASET_AT_UPLOAD is enabled, returns a dataset built from the
        ingested features for validation. Otherwise, returns None.

    Notes
    -----
    - Uses global tdfs4ds context such as FEATURE_STORE_TIME, RUN_ID, and PROCESS_TYPE.
    - Logs ingestion status in process follow-up tables.
    - Skips ingestion when existing completed results are found unless
      `force_compute=True`.
    - Applies Teradata-optimized storage and statistics collection.

    Raises
    ------
    ValueError
        If unsupported data types are found (CLOB/BLOB/JSON).
    Exception
        For ingestion failure or storage errors.

    Example
    -------
    >>> _upload_features(
    ...     df=dataframe,
    ...     entity_id="customer_id",
    ...     feature_names=["age", "credit_score"],
    ...     process_id="customer_features_v1",
    ...     force_compute=False
    ... )
    """
        
    from tdfs4ds.feature_store.entity_management        import register_entity
    from tdfs4ds.feature_store.feature_store_management import Gettdtypes
    from tdfs4ds.feature_store.feature_store_management import register_features
    from tdfs4ds.feature_store.feature_data_processing  import prepare_feature_ingestion
    from tdfs4ds.feature_store.feature_data_processing  import store_feature, apply_collect_stats
    from tdfs4ds.utils.info import get_column_types, update_varchar_length

    # Convert entity_id to a dictionary if not already
    if isinstance(entity_id, list):
        entity_id.sort()
        entity_id = get_column_types(df, entity_id)
        logger_safe("debug", "entity_id converted to dict: %s", entity_id)
    elif isinstance(entity_id, str):
        entity_id = get_column_types(df, [entity_id])
        logger_safe("debug", "entity_id converted to dict: %s", entity_id)

    # Map feature versions
    if isinstance(feature_versions, list):
        selected_features = dict(zip(feature_names, feature_versions))
    else:
        selected_features = {k: feature_versions for k in feature_names}

    # Get Teradata types for features
    feature_names_types = Gettdtypes(df, features_columns=feature_names, entity_id=entity_id)

    if force_varchar_length is not None:
        logger_safe("debug", "Updating VARCHAR lengths with force_varchar_length=%s", force_varchar_length)
        feature_names_types = update_varchar_length(
            feature_names_types,
            new_varchar_length=force_varchar_length
        )

    def validate_feature_types(feature_names_types):
        invalid = {
            k: v['type'] for k, v in feature_names_types.items()
            if any(x in v['type'].lower() for x in ['clob', 'blob', 'json'])
        }
        if invalid:
            raise ValueError(
                f"Unsupported data types found: {invalid}. "
                "CLOB/BLOB/JSON are not supported."
            )

    validate_feature_types(feature_names_types)

    logger_safe("info", "Registering entity %s in feature store", entity_id)
    register_entity(entity_id, feature_names_types, primary_index=primary_index, partitioning=partitioning)

    if getattr(tdfs4ds, "DEBUG_MODE", False):
        logger_safe(
            "debug",
            "_upload_features entity_id=%s null_substitute=%s features=%s primary_index=%s partitioning=%s",
            entity_id, entity_null_substitute, feature_names, primary_index, partitioning
        )
        logger_safe("debug", "selected_features=%s df.columns=%s", selected_features, df.columns)

    register_features(entity_id, feature_names_types, primary_index, partitioning)
    logger_safe("info", "Features registered in catalog: %s", feature_names)

    follow_up = None
    if process_id and tdfs4ds.FEATURE_STORE_TIME:
        follow_up = tdfs4ds.process_store.process_followup.follow_up_report()
        follow_up = follow_up[
            (follow_up.STATUS == 'COMPLETED') &
            (follow_up.VALIDTIME_DATE.isna() == False) &
            (follow_up.VALIDTIME_DATE == tdfs4ds.FEATURE_STORE_TIME) &
            (follow_up.PROCESS_ID == process_id)
        ]

    if filtermanager is None:
        do_compute = not (process_id and follow_up is not None and follow_up.shape[0] > 0)
        if not do_compute and not force_compute:
            logger_safe(
                "info",
                "Skipping computation for process_id=%s at time %s (already exists, force_compute=False)",
                process_id, tdfs4ds.FEATURE_STORE_TIME
            )
        if do_compute or force_compute:
            logger_safe("info", "Beginning feature ingestion for entity=%s", entity_id)
            tdfs4ds.process_store.process_followup.followup_open(
                run_id=tdfs4ds.RUN_ID,
                process_type=tdfs4ds.PROCESS_TYPE,
                process_id=process_id
            )
            try:
                prepared_features, volatile_table, features_infos = prepare_feature_ingestion(
                    df, entity_id, feature_names,
                    feature_versions=selected_features,
                    primary_index=primary_index,
                    entity_null_substitute=entity_null_substitute,
                    partitioning=partitioning
                )
                store_feature(entity_id, volatile_table, entity_null_substitute,
                              primary_index, partitioning, features_infos)
                apply_collect_stats(entity_id, primary_index, partitioning, features_infos)

                tdfs4ds.process_store.process_followup.followup_close(
                    run_id=tdfs4ds.RUN_ID,
                    process_type=tdfs4ds.PROCESS_TYPE,
                    process_id=process_id
                )
                logger_safe("info", "Feature ingestion completed for entity=%s", entity_id)

            except Exception as e:
                logger_safe("exception", "Feature ingestion failed for entity=%s", entity_id)
                tdfs4ds.process_store.process_followup.followup_close(
                    run_id=tdfs4ds.RUN_ID,
                    process_type=tdfs4ds.PROCESS_TYPE,
                    process_id=process_id,
                    status='FAILED,' + str(e).split('\n')[0]
                )
                raise

    else:

        logger_safe("info", "FilterManager detected: %s filters to process", filtermanager.nb_filters)
        something_computed = False
        pbar = tqdm(
            range(filtermanager.nb_filters),
            total=filtermanager.nb_filters,
            desc="Applying filters",
            unit="filter",
            leave=False
        )

        for i in pbar:
            filter_id = i + 1
            filtermanager.update(filter_id)

            try:
                pbar.set_description(f"Applying filter {filter_id}/{filtermanager.nb_filters}")

                # Convert datetime columns to string
                df_bar = filtermanager.display().to_pandas().astype(object)  # avoid conversion issues
                for col in df_bar.select_dtypes(include=["datetime", "datetimetz"]).columns:
                    df_bar[col] = df_bar[col].dt.strftime("%Y-%m-%d %H:%M:%S")

                # Convert to JSON object (dict)
                bar_info = df_bar.iloc[0].to_dict()

                # ---- ADD THIS: handle python date objects ----
                from datetime import date, datetime
                for key, value in bar_info.items():
                    if isinstance(value, (date, datetime)):  # convert date/datetime to string
                        bar_info[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                # ----------------------------------------------

                bar_info = str(bar_info)
                if len(bar_info) > 120:
                    bar_info = bar_info[:117] + "..."
                pbar.set_postfix_str(bar_info)

            except Exception:
                # postfix is optional; ignore errors from display() here
                pass

            logger_safe("debug", "Applying filter %s/%s:\n%s",
                i + 1, filtermanager.nb_filters, filtermanager.display())

            do_compute = True
            if process_id and tdfs4ds.FEATURE_STORE_TIME:
                # see if already computed
                follow_up = tdfs4ds.process_store.process_followup.follow_up_report(process_id=process_id, filtermanager=filtermanager)
                follow_up = follow_up[
                    (follow_up.STATUS == 'COMPLETED') &
                    (follow_up.VALIDTIME_DATE.isna() == False) &
                    (follow_up.VALIDTIME_DATE == tdfs4ds.FEATURE_STORE_TIME)
                    ]                
                
                if follow_up.shape[0] > 0:
                    do_compute = False

            if not do_compute and not force_compute:
                logger_safe(
                    "info",
                    "Skipping computation for process_id=%s at time %s (already exists, force_compute=False)",
                    process_id, tdfs4ds.FEATURE_STORE_TIME
                )
                pbar.colour = "green" 
            if do_compute or force_compute:
                pbar.colour = "blue" 
                tdfs4ds.process_store.process_followup.followup_open(
                    run_id        = tdfs4ds.RUN_ID,
                    process_type  = tdfs4ds.PROCESS_TYPE,
                    process_id    = process_id,
                    filtermanager = filtermanager
                )
                try:
                    prepared_features, volatile_table, features_infos = prepare_feature_ingestion(
                        df, entity_id, feature_names,
                        feature_versions       = selected_features,
                        primary_index          = primary_index,
                        entity_null_substitute = entity_null_substitute,
                        partitioning           = partitioning
                    )

                    store_feature(entity_id, volatile_table, entity_null_substitute,
                                  primary_index, partitioning, features_infos)
                    
                    something_computed = True

                    tdfs4ds.process_store.process_followup.followup_close(
                        run_id        = tdfs4ds.RUN_ID,
                        process_type  = tdfs4ds.PROCESS_TYPE,
                        process_id    = process_id,
                        filtermanager = filtermanager
                    )

                except Exception as e:
                    logger_safe("exception", "Error with filter iteration %s: %s", i + 1, str(e))
                    tdfs4ds.process_store.process_followup.followup_close(
                        run_id        = tdfs4ds.RUN_ID,
                        process_type  = tdfs4ds.PROCESS_TYPE,
                        process_id    = process_id,
                        status        = 'FAILED,' + str(e).split('\n')[0],
                        filtermanager = filtermanager
                    )
                    raise

        if something_computed:
            apply_collect_stats(entity_id, primary_index, partitioning, features_infos)

    if tdfs4ds.BUILD_DATASET_AT_UPLOAD:
        logger_safe("info", "Building dataset for validation...")
        try:
            return build_dataset(
                entity_id, selected_features,
                view_name=None,
                entity_null_substitute=entity_null_substitute
            )
        except Exception as e:
            logger_safe("error", "Dataset build failed: %s", str(e).split('\n')[0])
            logger_safe("error", "entity=%s features=%s", entity_id, selected_features)
    else:
        logger_safe("info", "Dataset build disabled (BUILD_DATASET_AT_UPLOAD=False)")
        return




def build_dataset(entity_id, selected_features, view_name, schema_name=None, comment=None, return_query=False,
                  feature_store_time=False, join_type='INNER'):
    """
    Generate a SQL query and create a Teradata view to retrieve records for the specified entity IDs based on selected features.

    Parameters:
    ----------
    entity_id : list, dict, or str
        The entity IDs for which records are needed. Can be a list, dictionary, or string.
        - If list: contains multiple entity IDs.
        - If dict: keys are the entity IDs.
        - If str: a single entity ID.

    selected_features : dict
        A dictionary where the keys are feature table names, and the values are lists of tuples
        (feature_id, feature_version, feature_name) specifying the features to retrieve.
        NOTE: feature_version may be either:
          - a single UUID string, or
          - a list of dicts like:
              {"process_id": <UUID>, "process_view_name": <str>}

    view_name : str
        The name of the view to be created in the database.

    schema_name : str, optional
        The name of the database schema where the view will be created.
        Defaults to the global `tdfs4ds.SCHEMA` if not provided.

    comment : str, optional
        A comment to attach to the created view for documentation purposes. Defaults to None.

    return_query : bool, optional
        If True, the function will return the SQL query string instead of executing it. Defaults to False.

    feature_store_time : bool, optional
        If True, the query will use a specific `VALIDTIME` based on `tdfs4ds.FEATURE_STORE_TIME`.
        If False, the query will use `CURRENT VALIDTIME`. Defaults to False.

    join_type : str, optional
        Specifies the type of join to use between features: 'INNER' (default) or 'FULL OUTER'.

    Returns:
    -------
    str or tdml.DataFrame
        - If `return_query` is True, returns the generated SQL query as a string.
        - Otherwise, returns a Teradata DataFrame containing the results.

    Raises:
    ------
    ValueError
        If an invalid `join_type` is provided.
    """

    # Validate the join type
    if join_type not in ['INNER', 'FULL OUTER']:
        tdfs4ds.logger.error(f"{join_type} is not valid. Only 'INNER' and 'FULL OUTER' are authorized.")
        raise ValueError("Invalid join type. Use 'INNER' or 'FULL OUTER'.")

    # Default schema fallback if not provided
    if schema_name is None:
        schema_name = tdfs4ds.SCHEMA

    from tdfs4ds.feature_store.feature_query_retrieval import get_feature_location

    # Define the VALIDTIME clause based on feature store time
    if feature_store_time:
        if tdfs4ds.FEATURE_STORE_TIME is None:
            validtime_statement = 'CURRENT VALIDTIME'
        else:
            validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"
    else:
        validtime_statement = 'CURRENT VALIDTIME'
    tdfs4ds.logger.info(f"VALIDTIME for the query: {validtime_statement}")

    # Retrieve the locations of features from the feature store
    tdfs4ds.logger.info("Retrieving the tables where the features are located.")
    list_features = get_feature_location(entity_id, selected_features)

    # Normalize entity_id into a list format for consistent processing
    if isinstance(entity_id, list):
        list_entity_id = entity_id
    elif isinstance(entity_id, dict):
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Sort the entity ID list for consistent query generation
    list_entity_id.sort()

    # Helpers
    import re
    def _sanitize_identifier(name: str) -> str:
        # Keep letters, numbers, and underscores; replace others with '_'
        return re.sub(r'[^0-9A-Za-z_]', '_', name)

    used_alias_counts = {}  # base_alias -> count

    def _unique_alias(base: str) -> str:
        """
        Ensure alias uniqueness: if base already used, append _2, _3, ...
        """
        if base not in used_alias_counts:
            used_alias_counts[base] = 1
            return base
        used_alias_counts[base] += 1
        return f"{base}_{used_alias_counts[base]}"

    # Initialize sub-query construction
    tdfs4ds.logger.info("Generating the sub-queries for feature retrieval.")
    sub_queries = []

    # Format entity ID columns for SQL query
    txt_entity = '\n ,'.join(['B1.' + e for e in list_entity_id])

    # Construct sub-queries for each feature
    for k, v in list_features.items():
        for feature_id, feature_version, feature_name in v:

            # Multiple processes: list of dicts
            if isinstance(feature_version, list):
                for item in feature_version:
                    process_id = item.get("process_id")
                    process_view_name = item.get("process_view_name") or "PROCESS"
                    base_alias = _sanitize_identifier(f"{feature_name}_{process_view_name}")
                    alias = _unique_alias(base_alias)

                    txt_where = f"(FEATURE_ID = {feature_id} AND FEATURE_VERSION='{process_id}')"
                    feature_str = ',B1.FEATURE_VALUE AS ' + alias

                    sub_queries.append(
                        {
                            'feature_name': alias,
                            'query': f"""
                            SEQUENCED VALIDTIME
                            SELECT 
                               {txt_entity}
                              {feature_str}
                            FROM {k} B1
                            WHERE {txt_where}
                            """
                        }
                    )

            # Single UUID
            else:
                base_alias = _sanitize_identifier(feature_name)
                alias = _unique_alias(base_alias)

                txt_where = f"(FEATURE_ID = {feature_id} AND FEATURE_VERSION='{feature_version}')"
                feature_str = ',B1.FEATURE_VALUE AS ' + alias
                sub_queries.append(
                    {
                        'feature_name': alias,
                        'query': f"""
                        SEQUENCED VALIDTIME
                        SELECT 
                           {txt_entity}
                          {feature_str}
                        FROM {k} B1
                        WHERE {txt_where}
                        """
                    }
                )

    # Handle case where no features are available
    if len(sub_queries) == 0:
        tdfs4ds.logger.warning("No features available for the specified entity IDs.")
        return

    # Generate SELECT clause for the final query
    if join_type == 'INNER':
        txt_entity = '\n ,'.join(['A1.' + e for e in list_entity_id])
    elif join_type == 'FULL OUTER':
        txt_entity = '\n ,'.join(
            [f"COALESCE({','.join(['A' + str(i) + '.' + e for i, _ in enumerate(sub_queries, 1)])}) AS {e}" for e in
             list_entity_id])

    select_query = f"""
          {txt_entity}
        , A1.{sub_queries[0]['feature_name']}
    """

    # Generate FROM and JOIN clauses for the final query
    from_query = f"""
    FROM ({sub_queries[0]['query']}) A1
    """

    for i, query_ in enumerate(sub_queries[1:], 2):
        # Add the feature to the SELECT clause
        select_query += f"\t, A{i}.{query_['feature_name']}\n"

        # Create the ON clause for joining on entity IDs
        on_clause = ' AND '.join(['A1.' + c + '= A' + str(i) + '.' + c for c in list_entity_id])

        # Add the join clause to the FROM section
        from_query += f"""
        {join_type} JOIN ({query_['query']}) A{i}
        ON {on_clause}
        """

    # Combine the clauses into the final query
    query = f"""
    {validtime_statement}
    SELECT {select_query}
    {from_query}
    """

    # Wrap the query as a view creation statement
    query = f"""
    REPLACE VIEW {schema_name}.{view_name} AS
    LOCK ROW FOR ACCESS
    {query}
    """
    tdfs4ds.logger.info(f"Creating the view {view_name} in the {schema_name} database.")
    tdml.execute_sql(query)

    # Add a comment to the created view, if provided
    if comment:
        tdfs4ds.logger.info(f"Adding a comment to the view {view_name} in the {schema_name} database.")
        tdml.execute_sql(f"COMMENT ON VIEW {schema_name}.{view_name} IS '{comment}'")

    # build the dataset object
    tdfs4ds.logger.info(f"Creation of the dataset object.")
    dataset = Dataset(view_name=view_name, schema_name=schema_name)
    tdfs4ds.logger.info(f"Registering of the dataset in the dataset catalog.")
    DatasetCatalog(schema_name=tdfs4ds.SCHEMA, name=tdfs4ds.DATASET_CATALOG_NAME).add_dataset(dataset=dataset)

    # Return the query or the DataFrame based on the `return_query` flag
    if return_query:
        tdfs4ds.logger.info("Returning the generated dataset query.")
        return query
    else:
        tdfs4ds.logger.info("Returning the dataset as a Teradata DataFrame.")
        return tdml.DataFrame.from_table(tdml.in_schema(schema_name, view_name))



def build_dataset_opt(entity_id, selected_features, view_name = None, schema_name=tdfs4ds.SCHEMA,
                  comment='dataset', no_temporal=False, time_manager=None, query_only=False, entity_null_substitute={},
                  other=None, time_column=None, filtermanager = None, filter_conditions = None
                  ):
    dataset = augment_source_with_features(
        source_schema       = None,
        source_name         = None,
        entity_id           = entity_id,
        feature_selection   = selected_features,
        output_view_name    = view_name,
        output_view_schema  = schema_name
    )

    return dataset

def augment_source_with_features(source_schema, source_name, entity_id, feature_selection, output_view_schema,
                                 output_view_name, join_type='LEFT JOIN'):
    """
    Augment a source table with selected features by creating a view that joins the source data
    with feature tables based on specified entity identifiers and feature selections. The join
    type can be specified as either 'LEFT JOIN' or 'INNER JOIN':

    - 'LEFT JOIN': Retains all rows from the source table, with missing values for unmatched features.
    - 'INNER JOIN': Returns only rows where all specified features have matching, non-missing values.

    Parameters:
    source_schema (str): The schema of the source table to augment.
    source_name (str): The name of the source table to augment.
    entity_id (str or list of str): The entity ID(s) for joining the source data with feature tables.
                                    Can be a single string or a list of strings.
    feature_selection (list): A list of features to select and join with the source data. Each feature
                              is represented as a tuple with (feature_id, feature_version).
    output_view_schema (str): The schema in which to create the output view.
    output_view_name (str): The name of the output view to create with augmented features.
    join_type (str, optional): The type of SQL join to use, either 'LEFT JOIN' for a full dataset
                               with possible missing values or 'INNER JOIN' for a dataset with
                               only complete feature matches. Defaults to 'LEFT JOIN'.

    Returns:
    tdml.DataFrame: A DataFrame object that references the newly created view with augmented features.
    """

    from tdfs4ds.feature_store.feature_query_retrieval import get_feature_location

    # Convert entity_id to a list if provided as a single string for consistency in handling
    if isinstance(entity_id, str):
        entity_id = [entity_id]

    # Retrieve feature locations (tables) for the selected features based on entity_id
    locations = get_feature_location(entity_id=entity_id, selected_features=feature_selection)

    # Initialize the SELECT part of the query with all columns from the source table
    query_select = f"""
    REPLACE VIEW {output_view_schema}.{output_view_name}
    AS LOCK ROW FOR ACCESS
    SELECT
        SOURCE.*
    """
    query_join = []  # To store the JOIN clauses for each feature
    counter = 1  # Counter for aliasing tables in joins

    # Loop through each feature table and the associated list of features
    for feature_store_view, list_features in locations.items():
        # Add each feature as a separate column selection with appropriate table alias
        for feature in list_features:
            table_name = 'A' + str(counter)  # Alias for the feature table in JOIN
            # Append the feature column to the SELECT clause with alias
            query_select += '\n, ' + table_name + '.' + feature[2]

            # Create the ON clause for joining on entity IDs between source and feature tables
            on_clause = ' AND '.join(['SOURCE.' + c + '=' + table_name + '.' + c for c in entity_id])

            # Construct the JOIN clause based on the specified join_type
            query_join.append(
                f"""
                {join_type} 
                (CURRENT VALIDTIME
                SEL
                    A.*
                  , A.FEATURE_VALUE AS {feature[2]}
                  FROM {feature_store_view} A
                  WHERE FEATURE_ID = {feature[0]} AND FEATURE_VERSION = '{feature[1]}'
                ) {table_name}
                ON {on_clause}
                """
            )
            counter += 1  # Increment the alias counter

    if source_schema is None and source_name is None:
        query_available_features, list_features = get_available_entity_id_records(entity_id, feature_selection)
        # Combine the SELECT and JOIN parts to form the complete SQL query
        query = query_select + '\n' + f'FROM ({query_available_features}) SOURCE \n' + '\n'.join(query_join)
    else:
        # Combine the SELECT and JOIN parts to form the complete SQL query
        query = query_select + '\n' + f'FROM {source_schema}.{source_name} SOURCE \n' + '\n'.join(query_join)

    # Execute the SQL query to create the augmented view
    tdml.execute_sql(query)

    # Return a DataFrame reference to the newly created view for further use
    try:
        return tdml.DataFrame.from_table(tdml.in_schema(output_view_schema, output_view_name))
    except Exception as e:
        print(str(e))
        return None


def upload_tdstone2_scores(model):
    """
    Uploads features from a model's predictions to the Teradata feature store. This function handles the entire
    workflow from extracting feature names and types, registering them in the feature catalog, preparing features for ingestion,
    storing them in the feature store, and finally creating a dataset view in the feature store.

    Parameters:
    - model: The model object whose predictions contain features to be uploaded. This model should have methods
      to extract predictions and feature information.

    Returns:
    - DataFrame: A DataFrame representing the dataset view created in the feature store, which includes
      features from the model's predictions.

    Note:
    - The function assumes that the model provides a method `get_model_predictions` which returns a Teradata DataFrame.
    - Entity ID for the model is extracted and registered in the data domain.
    - The function cleans up by dropping the volatile table created during the process.
    - The feature names and their types are extracted from the model's predictions and are registered in the feature catalog.
    """

    from tdfs4ds.feature_store.entity_management import register_entity
    from tdfs4ds.feature_store.entity_management import tdstone2_entity_id
    from tdfs4ds.feature_store.feature_store_management import tdstone2_Gettdtypes
    from tdfs4ds.feature_store.feature_store_management import register_features
    from tdfs4ds.feature_store.feature_data_processing import prepare_feature_ingestion_tdstone2
    from tdfs4ds.feature_store.feature_data_processing import store_feature

    # Extract the entity ID from the existing model.
    entity_id = tdstone2_entity_id(model)

    # Register the entity ID in the data domain.
    register_entity(entity_id)

    # Get the Teradata types of the features from the model's predictions.
    feature_names_types = tdstone2_Gettdtypes(model,entity_id)

    # Register these features in the feature catalog.
    register_features(entity_id, feature_names_types)

    # Prepare the features for ingestion into the feature store.
    if 'score' in [x[0] for x in inspect.getmembers(type(model))]:
        prepared_features, volatile_table_name = prepare_feature_ingestion_tdstone2(
            model.get_model_predictions(),
            entity_id
        )
    else:
        prepared_features, volatile_table_name = prepare_feature_ingestion_tdstone2(
            model.get_computed_features(),
            entity_id
        )

    # Store the prepared features in the feature store.
    store_feature(entity_id, prepared_features)

    # Clean up by dropping the temporary volatile table.
    tdml.execute_sql(f'DROP TABLE {volatile_table_name}')

    # Get the list of selected features for building the dataset view.
    if 'score' in [x[0] for x in inspect.getmembers(type(model))]:
        selected_features = model.get_model_predictions().groupby(['FEATURE_NAME', 'ID_PROCESS']).count().to_pandas()[
            ['FEATURE_NAME', 'ID_PROCESS']].set_index('FEATURE_NAME').to_dict()['ID_PROCESS']
    else:
        selected_features = model.get_computed_features().groupby(['FEATURE_NAME', 'ID_PROCESS']).count().to_pandas()[
            ['FEATURE_NAME', 'ID_PROCESS']].set_index('FEATURE_NAME').to_dict()['ID_PROCESS']

    # Build and return the dataset view in the feature store.
    dataset = build_dataset(entity_id, selected_features, view_name=None)
    return dataset


def roll_out(process_list, time_manager, time_id_start = 1, time_id_end = None, force_compute = False, force_display_logs = False):
    """
    Executes a series of processes for each date in a given list, managing time, computation settings, and logging.

    This function iterates over a range of time steps, updating a TimeManager object with each step, and then
    executes a list of processes for that time step. It also manages synchronization of time for the feature store
    and optionally controls forced computation and log display behavior.

    Parameters:
    - process_list (list): A list of process IDs that need to be executed for each time step.
    - time_manager (TimeManager): An object that manages time-related operations, like updating or retrieving time.
    - time_id_start (int, optional): The starting time step ID. Default is 1.
    - time_id_end (int, optional): The ending time step ID. If None, it will run until the last time step in the
      time manager.
    - force_compute (bool, optional): If True, forces each process to recompute even if previous results exist.
      Default is False.
    - force_display_logs (bool, optional): If True, forces log display during the rollout even if global log display
      is disabled. Default is False.

    Side Effects:
    - Temporarily modifies global variables DISPLAY_LOGS, PROCESS_TYPE, RUN_ID, and FEATURE_STORE_TIME.
    - Restores DISPLAY_LOGS setting after execution.
    - Catches and prints exceptions along with the time step on which they occurred.

    Steps performed:
    1. Disables display logs by default unless `force_display_logs` is True.
    2. Sets process type to 'ROLL_OUT' and initializes a unique run ID.
    3. Iterates over the specified range of time steps.
    4. Updates the time manager with the current time step.
    5. Synchronizes the feature store time with the current time step.
    6. Executes each process in the process list with optional forced computation.
    7. Restores original display log settings after completion.

    Example:
    >>> process_list = ['process_1', 'process_2']
    >>> time_manager = TimeManager(...)
    >>> roll_out(process_list, time_manager, time_id_start=1, time_id_end=10, force_compute=True, force_display_logs=True)
    """

    # Disable display logs
    temp_DISPLAY_LOGS = tdfs4ds.DISPLAY_LOGS
    tdfs4ds.DISPLAY_LOGS = False
    if force_display_logs:
        tdfs4ds.DISPLAY_LOGS = True
    PROCESS_TYPE = tdfs4ds.PROCESS_TYPE
    tdfs4ds.PROCESS_TYPE = 'ROLL_OUT'
    tdfs4ds.RUN_ID = str(uuid.uuid4())

    try:
        # Define range of time steps
        if time_id_end is None:
            time_range = range(time_id_start, time_manager.nb_time_steps + 1)
        else:
            time_range = range(time_id_start, min(time_manager.nb_time_steps + 1, time_id_end + 1))

        # Progress bar
        pbar = tqdm(time_range, desc="Starting rollout", unit="step")

        for i in pbar:
            # Update time manager
            time_manager.update(time_id=i)
            date_ = str(time_manager.display()['BUSINESS_DATE'].values[0])

            # Sync feature store time
            tdfs4ds.FEATURE_STORE_TIME = time_manager.get_date_in_the_past()

            # Display current progress in tqdm
            pbar.set_postfix(time=date_, feature_time=tdfs4ds.FEATURE_STORE_TIME)

            if tdfs4ds.DEBUG_MODE:
                print("roll_out | date_:", date_)
                print("roll_out | feature_store_time:", tdfs4ds.FEATURE_STORE_TIME)

            # Execute all processes for this time step
            for proc_id in process_list:
                pbar.set_description(f"Processing {date_} | proc {proc_id}")
                run(process_id=proc_id, force_compute=force_compute)

        # Restore settings
        tdfs4ds.DISPLAY_LOGS = temp_DISPLAY_LOGS

    except Exception as e:
        tdfs4ds.DISPLAY_LOGS = temp_DISPLAY_LOGS
        print(str(e).split('\n')[0])
        tdfs4ds.PROCESS_TYPE = PROCESS_TYPE
        raise

    tdfs4ds.PROCESS_TYPE = PROCESS_TYPE