import teradataml as tdml
import tdfs4ds
import uuid
import hashlib

def list_features():
    """
    Retrieves and returns a list of features from a feature store as a DataFrame.

    This function constructs a SQL query to fetch all features from a specific catalog view within a schema.
    The query uses the schema and catalog name configured in the `tdfs4ds` module. The function executes
    the query and returns the result as a DataFrame.

    Returns:
        tdml.DataFrame: A DataFrame containing the list of features from the feature store.

    Notes:
        - The function relies on the `tdfs4ds` module for configuration, including the `SCHEMA` and
          `FEATURE_CATALOG_NAME_VIEW` settings.
        - The `tdml.DataFrame` is used to execute the query and retrieve the data.
        - This function does not include temporal logic or filtering. It assumes the default behavior
          of querying the current valid state of the feature catalog.
    """
    return tdml.DataFrame(tdml.in_schema(tdfs4ds.SCHEMA, tdfs4ds.FEATURE_CATALOG_NAME_VIEW))

def generate_uuid_from_string(seed_string: str) -> str:
    # Use SHA-256 hash of the seed string to generate a unique seed
    seed_hash = hashlib.sha256(seed_string.encode()).hexdigest()

    # Use the first 32 characters of the hash as the seed for UUID
    namespace_uuid = uuid.UUID(seed_hash[:32])

    # Generate a UUID using the namespace UUID and the original seed string
    generated_uuid = uuid.uuid5(namespace_uuid, seed_string)

    return str(generated_uuid).replace('-','_')

def get_feature_store_table_name(entity_id, feature_type, data_domain=None, primary_index=None, partitioning=''):
    """
    Constructs names for a database table and a corresponding view within a feature store, using the provided entity attributes, feature type, optional data domain, primary index, and partitioning information.

    This function generates names that are intended for organizing and accessing features in a structured manner within a feature store. The naming convention integrates various elements, including a prefix (indicating tables or views), the specified data domain (or a default one), and aspects of the entity ID, ensuring uniqueness and clarity in the schema.

    Parameters:
    - entity_id (dict, list, str, int): The identifier(s) for the entity. This can be:
        - a dictionary with keys representing entity attributes,
        - a list of attributes, or
        - a single attribute (string or integer).
      The function constructs the base part of the table and view names differently based on the type of `entity_id`.
    - feature_type (str): Specifies the type of feature, contributing to the naming to indicate the kind of data stored.
    - data_domain (str, optional): The categorization under which the table and view will be organized. If not provided, a default value from `tdfs4ds.DATA_DOMAIN` is used.
    - primary_index (list, optional): Specifies the primary index attributes. If not provided, it defaults to the attributes derived from `entity_id`. This influences the order and inclusion of entity attributes in the name.
    - partitioning (str, optional): A string containing attributes used for partitioning, separated by spaces or commas. This affects how the name indicates the data partitioning strategy.

    Returns:
    - tuple: Contains two strings; the first is the table name, and the second is the view name. These are constructed based on the input parameters to fit within a feature store's schema.

    Example:
    - For `entity_id={'customer_id': 123}`, `feature_type='purchase_history'`, `data_domain='retail'`, `primary_index=['customer_id']`, and `partitioning='year, month'`, this function would generate names like 'FS_T_retail_CUSTOMER_ID__YEAR_MONTH__PURCHASE_HISTORY' and 'FS_V_retail_CUSTOMER_ID__YEAR_MONTH__PURCHASE_HISTORY'.

    Note:
    - Assumes the presence of a `tdfs4ds` module with a `DATA_DOMAIN` constant for default data domain usage.
    - Designed for flexibility in entity ID specification, supporting simple IDs, attribute lists, or attribute key dictionaries.
    """
    import re

    # Set the data domain to the default if not specified
    if data_domain is None:
        data_domain = tdfs4ds.DATA_DOMAIN

    # Prepare entity ID list based on its type for further processing
    if isinstance(entity_id, list):
        list_entity_id = entity_id
    elif isinstance(entity_id, dict):
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Normalize entity ID attributes to uppercase for consistency
    entity_id_list = [x.upper() for x in list_entity_id]
    entity_id_list.sort()

    # Set primary index based on entity_id_list if not provided, then sort and normalize
    if primary_index is None:
        primary_index = entity_id_list
    elif type(primary_index) == str:
        primary_index = primary_index.split(',')
    primary_index = [x.upper() for x in primary_index]
    primary_index.sort()

    # Determine partitioning and other attributes for inclusion in the names
    partitioning_names = [k for k in entity_id_list if re.search(r'\b' + re.escape(k.upper()) + r'\b', partitioning.upper())]
    other_names = [k for k in entity_id_list if (k not in partitioning_names and k not in primary_index)]

    if tdfs4ds.DEBUG_MODE:
        print('get_feature_store_table_name','data_domain', data_domain)
        print('get_feature_store_table_name','primary_index', primary_index)
        print('get_feature_store_table_name','partitioning', partitioning)
        print('get_feature_store_table_name','partitioning_names',partitioning_names)
        print('get_feature_store_table_name','other_names',other_names)
    root_name = data_domain + '_' + '_'.join(primary_index)
    if partitioning != '' and len(partitioning_names)>0:
        root_name += '__' + '_'.join(partitioning_names)
    if len(other_names)>0:
        root_name += '__' + '_'.join(other_names)

    if tdfs4ds.DEBUG_MODE: print('root_name (before): ', root_name)
    root_name += '_' + feature_type
    root_name = generate_uuid_from_string(root_name)
    if tdfs4ds.DEBUG_MODE: print('root_name (after) : ', root_name)

    

    table_name = 'FS_T_' + root_name
    view_name  = 'FS_V_' + root_name

    return table_name, view_name


def get_available_features(entity_id, display_details=False):
    """
    Retrieves the names of available features for a given entity ID from a feature store.

    This function constructs and executes a SQL query to select feature names from a specific catalog within a schema
    for a given entity ID, optionally using a specific valid time if set in `tdfs4ds.FEATURE_STORE_TIME`. The function
    supports querying features as of a certain timestamp or the current valid time if no timestamp is specified. It
    also provides an option to display detailed information about the features.

    Parameters:
        entity_id (str, list, or dict): The ID of the entity for which to retrieve available features. This can be a
                                        single ID (str), a list of IDs, or a dictionary of IDs where keys are entity
                                        names and values are their corresponding IDs.
        display_details (bool, optional): If True, prints detailed information about all features in the catalog.
                                          Defaults to False.

    Returns:
        list: A list of feature names available for the specified entity ID.

    Note:
        - `tdfs4ds` is assumed to be a configuration module or object containing settings for the feature store,
          including `FEATURE_STORE_TIME`, `SCHEMA`, `FEATURE_CATALOG_NAME`, `DATA_DOMAIN`, and `DEBUG_MODE`.
        - The entity ID(s) are used to filter the features specific to the entity. If `entity_id` is a dictionary,
          the keys are considered as entity names, and their values are IDs. If it's a list, it's assumed to be a list
          of entity names or IDs. For a single string, it is treated as a single entity name or ID.
        - `FEATURE_STORE_TIME` is used to determine the temporal context for querying the feature data. If it is None,
          the query defaults to the current valid time.
        - If `DEBUG_MODE` is enabled in `tdfs4ds`, the constructed query is printed to the console.
        - The function uses `tdml.DataFrame.from_query` to execute the SQL query and `to_pandas` to convert the result
          into a pandas DataFrame for further processing.
    """
    if tdfs4ds.FEATURE_STORE_TIME == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"

    if type(entity_id) == dict:
        ENTITY_ID__ = ','.join([k.lower() for k, v in entity_id.items()])
    elif type(entity_id) == list:
        ENTITY_ID__ = ','.join([k.lower() for k in entity_id])
    else:
        ENTITY_ID__ = entity_id.lower()

    query = f"""
    {validtime_statement}
    SELECT 
          FEATURE_NAME
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME}
    WHERE LOWER(ENTITY_NAME) = '{ENTITY_ID__}'
    AND DATA_DOMAIN = '{tdfs4ds.DATA_DOMAIN}'
    """

    if tdfs4ds.DEBUG_MODE:
        print(query)

    if display_details:
        print(tdml.DataFrame.from_query(f'{validtime_statement} SELECT * FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME}'))

    return list(tdml.DataFrame.from_query(query).to_pandas().FEATURE_NAME.values)

def get_list_entity(domain=None):
    """
    Retrieve a list of unique entity names from a specified data domain.

    This function executes a database query to extract distinct entity names from
    a feature catalog, filtered by the provided data domain. If no domain is
    specified, it defaults to a predefined data domain.

    Parameters:
    domain (str, optional): The data domain to filter the entity names.
                            Defaults to None, in which case a predefined domain is used.

    Returns:
    DataFrame: A pandas-like DataFrame containing the unique entity names.
    """

    if tdfs4ds.FEATURE_STORE_TIME == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"

    # Use the default data domain if none is specified
    if domain is None:
        domain = tdfs4ds.DATA_DOMAIN

    # Constructing the SQL query to fetch distinct entity names from the specified domain
    query = f"{validtime_statement} SEL DISTINCT ENTITY_NAME FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} where DATA_DOMAIN = '{domain}'"

    # Executing the query and returning the result as a DataFrame
    return tdml.DataFrame.from_query(query)


def get_list_features(entity_name, domain=None):
    """
    Retrieve a list of feature names associated with a specific entity or entities
    from a given data domain.

    This function constructs and executes a database query to extract feature names
    for the specified entity or entities from a feature catalog, filtered by the
    provided data domain. If no domain is specified, it defaults to a predefined
    data domain.

    Parameters:
    entity_name (str or list): The name of the entity or a list of entity names
                               to fetch features for.
    domain (str, optional): The data domain to filter the feature names.
                            Defaults to None, where a predefined domain is used.

    Returns:
    DataFrame: A pandas-like DataFrame containing the feature names associated with the given entity or entities.
    """

    if tdfs4ds.FEATURE_STORE_TIME == None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"

    # Default to a predefined data domain if none is provided
    if domain is None:
        domain = tdfs4ds.DATA_DOMAIN

    # Convert the entity_name to a string if it is a list
    if type(entity_name) == list:
        entity_name = ','.join(entity_name)

    # Constructing the SQL query to fetch feature names for the specified entity or entities
    query = f"{validtime_statement} SEL FEATURE_NAME FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME} where entity_name = '{entity_name}' AND DATA_DOMAIN = '{domain}'"

    # Executing the query and returning the result as a DataFrame
    return tdml.DataFrame.from_query(query)


def get_feature_versions(entity_name, features, domain=None):
    """
    Retrieve version identifiers for one or more features belonging to a given entity.

    The function queries the underlying metadata tables to find the *process*
    (i.e., feature‑version) records that match the supplied entity and feature
    names.  It returns a mapping from each requested feature name to either:

    * **None** – if no matching rows were found.
    * A single UUID string – if exactly one matching row exists for the feature.
    * A list of dictionaries – if more than one matching row is found; each
      dictionary contains:
        ``process_id``          – the UUID of the process that produced the
                                  version,
        ``process_view_name``   – the human‑readable view name associated with
                                  that process.

    Parameters
    ----------
    entity_name : str | list[str]
        The name (or names) of the entity whose features we are querying.
        If a single string is supplied it is treated as a singleton list.

    features : str | list[str]
        One or more feature names to look up.  Accepts a single string or
        an iterable of strings; if a single string is provided it is wrapped in
        a list internally.

    domain : str, optional
        The data‑domain partition to filter on.  If omitted the default
        ``tdfs4ds.DATA_DOMAIN`` constant is used.

    Returns
    -------
    dict[str, str | None | list[dict]]
        A dictionary keyed by feature name.  Each value is either:
            * ``None`` – no records were found for that feature.
            * ``str`` – a single UUID string when exactly one row matched.
            * ``list[dict]`` – multiple matches; each dict has keys
              ``process_id`` and ``process_view_name``.

    Notes
    -----
    * The query joins the feature catalog view with the process catalog
      (specifically the “feature split” view) on data domain, entity ID,
      and feature name.
    * SQL string literals are escaped by doubling single quotes; this is a
      lightweight escape that suffices for the current use‑case.
    * The function preserves insertion order of features in the returned
      dictionary (Python 3.7+ guarantees dict order).
    * When ``tdfs4ds.DEBUG_MODE`` is true, the generated SQL statement is
      printed to stdout – useful for troubleshooting.

    Example
    -------
    >>> get_feature_versions('user', ['age', 'income'])
    {'age': 'c1d2e3f4-...', 'income': None}

    """


    # Normalize inputs
    if isinstance(features, str):
        features = [features]

    if isinstance(entity_name, str):
        entity_name = [entity_name]

    if domain is None:
        domain = tdfs4ds.DATA_DOMAIN

    # Basic escaping for single quotes in values used in SQL literals
    def _esc(s: str) -> str:
        return s.replace("'", "''")

    features_lits = ",".join(f"'{_esc(f)}'" for f in features)

    entity_name.sort()
    entity_name_str = ','.join(entity_name)

    query = f"""
        SELECT
            A.FEATURE_NAME
        ,   B.PROCESS_ID AS FEATURE_VERSION
        ,   B.VIEW_NAME AS PROCESS_VIEW_NAME
        FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW} A
        INNER JOIN {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME_VIEW_FEATURE_SPLIT} B
        ON A.DATA_DOMAIN = B.DATA_DOMAIN
        AND A.ENTITY_NAME = B.ENTITY_ID 
        AND A.FEATURE_NAME = B.FEATURE_NAME
        WHERE A.DATA_DOMAIN = '{domain}'
        AND A.ENTITY_NAME = '{entity_name_str}'
        AND A.FEATURE_NAME IN ({features_lits})
    """

    if tdfs4ds.DEBUG_MODE:
        print(query)

    rows = tdml.execute_sql(query).fetchall()

    # Initialize result for all requested features
    result = {f: None for f in features}

    # Collect (version, view) per feature, deduplicating while preserving order
    tmp = {f: [] for f in features}
    seen = {f: set() for f in features}

    for feat, version, view_name in rows:
        key = (version, view_name)
        if key not in seen.setdefault(feat, set()):
            seen[feat].add(key)
            tmp.setdefault(feat, []).append(key)

    # Shape:
    # - if exactly one row: return UUID string
    # - if multiple rows: list of {"process_id": <uuid>, "process_view_name": <str>}
    for feat in result:
        pairs = tmp.get(feat, [])
        if len(pairs) == 0:
            result[feat] = None
        elif len(pairs) == 1:
            result[feat] = pairs[0][0]  # UUID only
        else:
            result[feat] = [
                {"process_id": ver, "process_view_name": view}
                for (ver, view) in pairs
            ]

    return result


def get_entity_tables(entity_id, data_domain=None):
    """
    Retrieves a list of table names associated with a given entity ID or IDs from a feature catalog within a specific data domain.

    This function constructs and executes an SQL query to select distinct table names from a feature catalog that match the given entity ID(s) and data domain. If the data domain is not specified, it defaults to the system's default data domain. The entity ID can be a single string or a list of strings. If `DEBUG_MODE` is enabled in the system, the function prints the SQL query before execution.

    Parameters:
    - entity_id (str or list of str): The ID or IDs of the entities for which to retrieve table names.
    - data_domain (str, optional): The data domain within which to search for the entity IDs. Defaults to the system's default data domain if None.

    Returns:
    - list of str: A list of unique table names (in the format 'FEATURE_DATABASE.FEATURE_TABLE') associated with the given entity ID(s) within the specified data domain.

    Exceptions:
    - If the SQL query execution fails, the function attempts to retrieve the table names by converting the query results into a pandas DataFrame and then extracting the table names from it.

    Note:
    - This function depends on the external modules `tdfs4ds` and `tdml` for database schema details, default configurations, and SQL execution.
    """

    if data_domain is None:
        data_domain = tdfs4ds.DATA_DOMAIN

    if type(entity_id) == str:
        entity_id = [entity_id]

    query = f"""
    SELECT DISTINCT
    FEATURE_DATABASE || '.' || FEATURE_TABLE AS table_name
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW}
    WHERE ENTITY_NAME = '{','.join([k for k in entity_id])}'
    AND DATA_DOMAIN = '{data_domain}'
    """

    if tdfs4ds.DEBUG_MODE == True:
        print(query)

    try:
        table_list = [x[0] for x in tdml.execute_sql(query).fetchall()]
    except Exception as e:
        table_list = tdml.DataFrame.from_query(query).to_pandas().table_name.values

    return table_list

def get_feature_store_content(entity_id, data_domain=None, convert_to_date=False, time_manager = None, condition = '<='):
    """
    Retrieves content from a feature store for a given entity ID or IDs within a specified data domain, with options to convert datetime columns to dates, filter data based on a time management table, and apply a specific condition for the filter.

    This function first retrieves a list of table names associated with the given entity ID(s) in the specified data domain using the `get_entity_tables` function. It then constructs SQL queries to select distinct records from these tables, focusing on the 'ValidStart' column and the entity ID(s). If `convert_to_date` is True, it converts 'ValidStart' datetime values to date values in the queries. Additionally, if a `time_manager` object is provided, the function filters records in each table to include only those where 'ValidStart' meets the specified condition (e.g., before, on, or after) relative to the business date specified in the `time_manager`'s table. The condition for comparison is specified by the `condition` parameter.

    Parameters:
    - entity_id (str or list of str): The ID or IDs of the entities for which to retrieve content.
    - data_domain (str, optional): The data domain within which to search for the entity IDs. Defaults to the system's default data domain if None.
    - convert_to_date (bool, optional): Flag indicating whether to convert 'ValidStart' datetime values to date values. Defaults to False.
    - time_manager (object, optional): An object that specifies the schema and table name of a time management table to filter records based on business date. The object should have `schema_name` and `table_name` attributes, as well as a `data_type` indicating the type of data (e.g., date, datetime).
    - condition (str, optional): A string specifying the condition to apply to the 'ValidStart' column when filtering records based on the business date from the time management table. Defaults to '<='.

    Returns:
    - DataFrame: A DataFrame containing the retrieved content, with the 'ValidStart' column and the entity ID(s) from each table in the feature store that matches the criteria, optionally filtered by business date and specific condition.

    Note:
    - If `DEBUG_MODE` is enabled in the system, the function prints the constructed SQL query before execution.
    - This function leverages the `tdml` module for executing the SQL query and returning the results as a DataFrame.
    - The function adapts its behavior based on the presence and specifications of the `time_manager` object and the `condition` parameter to provide flexible data retrieval options.
    """
    if data_domain is None:
        data_domain = tdfs4ds.DATA_DOMAIN
    if type(entity_id) == str:
        entity_id = [entity_id]
    table_list = get_entity_tables(entity_id, data_domain)

    if time_manager is None:
        if convert_to_date:
            query = '\nUNION\n'.join(
                [f"SELECT DISTINCT CAST(ValidStart AS DATE) AS ValidStart, {','.join([k for k in entity_id])} FROM {x}" for x in table_list])
        else:
            query = '\nUNION\n'.join(
                [f"SELECT DISTINCT ValidStart, {','.join([k for k in entity_id])} FROM {x}" for x in table_list])
    else:
        if 'date' in time_manager.data_type.lower():
            if convert_to_date:
                query = '\nUNION\n'.join(
                    [f"SELECT DISTINCT CAST(ValidStart AS DATE) AS ValidStart, {','.join([k for k in entity_id])} FROM {x} WHERE CAST(ValidStart AS DATE) {condition} (SEL BUSINESS_DATE FROM {time_manager.schema_name}.{time_manager.table_name})" for x in table_list])
            else:
                query = '\nUNION\n'.join(
                    [f"SELECT DISTINCT ValidStart, {','.join([k for k in entity_id])} FROM {x} WHERE CAST(ValidStart AS DATE) {condition} (SEL BUSINESS_DATE FROM {time_manager.schema_name}.{time_manager.table_name})" for x in table_list])
        else:
            if convert_to_date:
                query = '\nUNION\n'.join(
                    [f"SELECT DISTINCT CAST(ValidStart AS DATE) AS ValidStart, {','.join([k for k in entity_id])} FROM {x} WHERE ValidStart {condition} (SEL BUSINESS_DATE FROM {time_manager.schema_name}.{time_manager.table_name})" for x in table_list])
            else:
                query = '\nUNION\n'.join(
                    [f"SELECT DISTINCT ValidStart, {','.join([k for k in entity_id])} FROM {x} WHERE ValidStart {condition} (SEL BUSINESS_DATE FROM {time_manager.schema_name}.{time_manager.table_name})" for x in table_list])

    if tdfs4ds.DEBUG_MODE == True:
        print(query)

    return tdml.DataFrame.from_query(query)


def get_feature_location(entity_id, selected_features):
    """
    Retrieve the location of selected features for given entity IDs.

    Parameters:
    entity_id (list, dict, or str): The entity IDs for which feature locations are needed. Can be a list, dictionary, or string.
    selected_features (dict): A dictionary of selected features with their versions.

    Returns:
    DataFrame: A pandas DataFrame containing the feature locations.
    """

    from tdfs4ds.utils.query_management import execute_query

    # Retrieve feature data from the feature catalog table
    feature_catalog = tdml.DataFrame.from_query(
        f'SELECT * FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME_VIEW}')

    # Convert entity_id to a list format for processing
    if isinstance(entity_id, list):
        list_entity_id = entity_id
    elif isinstance(entity_id, dict):
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Sort the entity ID list
    list_entity_id.sort()

    # Compose the entity names and retrieve the corresponding feature locations
    ENTITY_NAMES = ','.join([k for k in list_entity_id])
    ENTITY_ID = ', \n'.join([k for k in list_entity_id])

    # Construct ENTITY_ID_ based on the selected features
    if len(selected_features) > 1:
        ENTITY_ID_ = ','.join(['COALESCE(' + ','.join(
            ['AA' + str(i + 1) + '.' + k for i, c in enumerate(selected_features)]) + ') as ' + k for k in
                               list_entity_id])
    else:
        ENTITY_ID_ = ','.join(
            [','.join(['AA' + str(i + 1) + '.' + k for i, c in enumerate(selected_features)]) + ' as ' + k for k in
             list_entity_id])

    # Filter the feature catalog to get the feature location
    feature_location = feature_catalog[
        (feature_catalog.FEATURE_NAME.isin(list(selected_features.keys()))) &
        (feature_catalog.ENTITY_NAME == ENTITY_NAMES) &
        (feature_catalog.DATA_DOMAIN == tdfs4ds.DATA_DOMAIN)
        ].to_pandas()

    # Manage the case sensitivity
    feature_location['FEATURE_NAME_UPPER'] = [x.upper() for x in feature_location['FEATURE_NAME']]
    feature_location['FEATURE_VERSION'] = feature_location['FEATURE_NAME_UPPER'].map(
        {k.upper(): v for k, v in selected_features.items()})

    list_features = dict()
    # Group the feature locations by FEATURE_DATABASE and FEATURE_VIEW
    for location, df in feature_location.groupby(['FEATURE_DATABASE', 'FEATURE_TABLE']):
        list_features[f'"{location[0]}"."{location[1]}"'] = [(feature_id, feature_version, feature_name) for
                                                             feature_id, feature_version, feature_name in
                                                             zip(df.FEATURE_ID.values, df.FEATURE_VERSION.values,
                                                                 df.FEATURE_NAME.values)]

    return list_features

def write_where_clause_filter(filtermanager, filter_conditions, list_entity_id, filter_alias='FILTER', table_alias='A'):
    """
    Constructs a SQL WHERE clause based on filter criteria.

    This function generates a SQL WHERE clause for filtering records in a database. The `filter_conditions` parameter is
    a dictionary containing key-value pairs, where each key corresponds to a column name in `filtermanager.col_names`,
    and each value is an entity ID or filter value. The clause is constructed using aliases for the table and filter
    provided through `filter_alias` and `table_alias`.

    Parameters:
        filtermanager (object): An object that contains a `col_names` attribute, which is a list of valid column names
                                used for validation against the keys in the `filter` dictionary.
        filter_conditions (dict): A dictionary where keys represent column names that must match `filtermanager.col_names`, and values
                       represent entity IDs or specific filter values.
        list_entity_id (list): A list of entity IDs used to validate or restrict values in the filter dictionary.
        filter_alias (str, optional): The alias used for the filter table in the SQL query. Defaults to 'FILTER'.
        table_alias (str, optional): The alias used for the main table in the SQL query. Defaults to 'A'.

    Returns:
        str: A SQL WHERE clause string that joins each column and entity ID in `filter` using the format
             `<filter_alias>.<column> = <table_alias>.<value>` with 'AND' operators.

    Raises:
        ValueError: If any key in `filter` is not found in `filtermanager.col_names` or if any value in `filter`
                    is not in `list_entity_id`.

    Example:
        >>> filtermanager.col_names = ['column1', 'column2']
        >>> filter_conditions = {'column1': 'entity_id1', 'column2': 'entity_id2'}
        >>> list_entity_id = ['entity_id1', 'entity_id2']
        >>> write_where_clause_filter(filtermanager, filter_conditions, list_entity_id)
        'FILTER.column1=A.entity_id1 AND FILTER.column2=A.entity_id2'
    """

    # Validate keys in filter against filtermanager.col_names
    invalid_keys = [k for k in filter_conditions if k not in filtermanager.col_names]
    if invalid_keys:
        raise ValueError(f"Invalid filter keys found: {invalid_keys}. Keys must be in {filtermanager.col_names}.")

    # Validate values in filter against list_entity_id
    invalid_values = [v for v in filter_conditions.values() if v not in list_entity_id]
    if invalid_values:
        raise ValueError(f"Invalid filter values found: {invalid_values}. Values must be in {list_entity_id}.")

    # Construct the WHERE clause
    where_clause = ' AND '.join([f"{filter_alias}.{k} = {table_alias}.{v}" for k, v in filter_conditions.items()])

    return where_clause
def get_available_entity_id_records(entity_id, selected_features, other=None, time_column=None, filtermanager=None, filter_conditions=None):
    """
    Generate a SQL query to retrieve records for available entity IDs based on selected features.

    Parameters:
    entity_id (list, dict, or str): The entity IDs for which records are needed. Can be a list, dictionary, or string.
    selected_features (dict): A dictionary of selected features with their versions.
    other (optional): An additional DataFrame object for more complex queries. Defaults to None.
    time_column (str, optional): The name of the time column to use for temporal conditions. Defaults to None.

    Returns:
    tuple: A tuple containing:
        - str: A SQL query string to retrieve records for available entity IDs.
        - dict: A dictionary of the list of features and their locations.
    """


    if tdfs4ds.FEATURE_STORE_TIME is None:
        validtime_statement = 'CURRENT VALIDTIME'
    else:
        validtime_statement = f"VALIDTIME AS OF TIMESTAMP '{tdfs4ds.FEATURE_STORE_TIME}'"

    if other is not None:
        validtime_statement = ''

    # Get the feature locations for the given entity IDs and selected features
    list_features = get_feature_location(entity_id, selected_features)

    # Convert entity_id to a list format for processing
    if isinstance(entity_id, list):
        list_entity_id = entity_id
    elif isinstance(entity_id, dict):
        list_entity_id = list(entity_id.keys())
    else:
        list_entity_id = [entity_id]

    # Sort the entity ID list
    list_entity_id.sort()

    # Determine the time condition based on the presence of the 'other' DataFrame and time_column
    if other is not None:
        if 'date' in tdfs4ds.utils.info.get_column_types(df=other, columns=time_column)[time_column].lower():
            time_condition = f"AND PERIOD(CAST(ValidStart AS DATE), CAST(ValidEnd AS DATE)) CONTAINS B2.{time_column}"
        else:
            time_condition = f"AND PERIOD(ValidStart, ValidEnd) CONTAINS B2.{time_column}"

    # Initialize the query list
    query = []
    for k, v in list_features.items():
        # Construct the entity ID part of the query
        txt_entity = '\n ,'.join(list_entity_id)
        txt_entity_2 = '\n ,'.join(['B1.'+e for e in list_entity_id])
        # Apply filter condition
        if filtermanager is not None:
            filter_whereclause = write_where_clause_filter(
                filtermanager=filtermanager,
                list_entity_id=list_entity_id,
                filter_conditions=filter_conditions,
                table_alias='B1',
                filter_alias='FILTER'
            )
            filter_whereclause = ' AND ' + filter_whereclause
            filter_ = ',' + filtermanager.view_name + ' FILTER'
        else:
            filter_whereclause = ''
            filter_ = ''
        # Construct the WHERE clause for the query
        sub_query = []
        for feature_id, feature_version, _ in v:
            txt_where = f"(FEATURE_ID = {feature_id} AND FEATURE_VERSION='{feature_version}')"
            if other is None:
                sub_query.append(
                    f"""
                    SELECT 
                      {txt_entity_2}
                    FROM {k} B1
                    {filter_}
                    WHERE {txt_where}
                    {filter_whereclause}
                    """
                )
            else:
                sub_query.append(
                    f"""
                    SELECT
                      B2.{time_column}
                      ,{txt_entity_2}
                    FROM {k} B1
                    , {other._table_name} B2
                    {filter_}
                    WHERE ({txt_where})
                    {time_condition}
                    {filter_conditions}
                    """
                )
        sub_query = ' UNION ALL \n'.join(sub_query)


        # Append the query for the current feature location
        if other is None:
            query.append(
                f"""
                SELECT DISTINCT {txt_entity}
                FROM (
                    {validtime_statement}
                    {sub_query}
                ) B
                """
            )
        else:
            txt_entity_2 = '\n,'.join(['B1.'+c for c in txt_entity.split(',')])
            query.append(
                f"""
                SELECT
                 {time_column}
                ,{txt_entity}
                FROM (
                    {validtime_statement}
                    {sub_query}
                ) B
                """
            )

    # Join all individual queries with UNION and return
    return ' UNION '.join(query), list_features
