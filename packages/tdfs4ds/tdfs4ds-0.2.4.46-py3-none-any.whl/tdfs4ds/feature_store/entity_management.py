import inspect
from tdfs4ds.feature_store.feature_store_management import feature_store_table_creation
import tdfs4ds
import teradataml as tdml
import tqdm

def register_entity(entity_id, feature_types, primary_index = None, partitioning = ''):
    """
    Registers an entity within the feature store by facilitating the creation of feature store tables across multiple data types.

    This function leverages the `feature_store_table_creation` function to create feature store tables tailored for different data types: 'FLOAT', 'BIGINT', 'VARCHAR_UNICODE', and 'VARCHAR_LATIN'. By doing so, it ensures a comprehensive setup for the specified entity, allowing for a diverse range of feature data types to be stored efficiently.

    Parameters:
    - entity_id (str): Unique identifier for the entity. This ID is utilized to construct table names and associate them with the corresponding entity within the feature store.
    - primary_index (list, optional): Specifies the columns to be used as the primary index for the tables. A well-chosen primary index can significantly enhance query performance.
    - partitioning (str, optional): Defines the partitioning strategy for the tables, which can help manage and optimize the storage and retrieval of large datasets.

    Returns:
    tuple: Contains the names of the created feature store tables. This tuple includes names for tables designed to store 'FLOAT', 'BIGINT', 'VARCHAR_UNICODE', and 'VARCHAR_LATIN' feature types, in the order they were created.

    Example Usage:
    >>> register_entity("customer123")
    ('customer123_float_table', 'customer123_bigint_table', 'customer123_varchar_unicode_table', 'customer123_varchar_latin_table')

    Note:
    - This function is integral to initializing the feature storage for a new entity, ensuring that data of various types can be accommodated.
    - The function assumes that the `feature_store_table_creation` function handles the intricacies of table creation, including dealing with existing tables based on the 'if_exists' parameter and applying specified partitioning and indexing strategies.
    """

    feature_types = list(set([v['type'] for k,v in feature_types.items()]))
    for feature_type in feature_types:
        feature_store_table_creation(entity_id, feature_type=feature_type, primary_index = primary_index, partitioning=partitioning)
    
    return
    # feature_store_table_name_float           = feature_store_table_creation(entity_id, feature_type='FLOAT', primary_index = primary_index, partitioning=partitioning)
    # feature_store_table_name_integer         = feature_store_table_creation(entity_id, feature_type='BIGINT', primary_index = primary_index, partitioning=partitioning)
    # feature_store_table_name_varchar_unicode = feature_store_table_creation(entity_id, feature_type='VARCHAR_UNICODE', primary_index = primary_index, partitioning=partitioning)
    # feature_store_table_name_varchar_latin   = feature_store_table_creation(entity_id, feature_type='VARCHAR_LATIN', primary_index = primary_index, partitioning=partitioning)
    # feature_store_table_name_decimal         = feature_store_table_creation(entity_id, feature_type='DECIMAL', primary_index=primary_index, partitioning=partitioning)

    # return feature_store_table_name_float,feature_store_table_name_integer,feature_store_table_name_varchar_unicode, feature_store_table_name_varchar_latin, feature_store_table_name_decimal

def tdstone2_entity_id(existing_model):
    """
    Generate a dictionary mapping entity IDs to their respective data types in a given tdstone2 model.

    This function analyzes the provided tdstone2 model object to determine the type of the model ('model scoring' or 'feature engineering').
    Depending on the model type, it retrieves the list of entity IDs from the appropriate mapper attribute ('mapper_scoring' or 'mapper').
    It then constructs a dictionary where each key is an entity ID, and its corresponding value is the data type of that entity ID,
    as specified in the model's mapper attributes ('types').

    Args:
        existing_model (object): A model object created using the tdstone2 package.
                                 This object should contain the necessary mapper attributes ('mapper_scoring' or 'mapper') with 'id_row', 'id_partition', and 'types'.

    Returns:
        dict: A dictionary mapping entity IDs to their data types.
              Keys are entity IDs, and values are data types (e.g., 'BIGINT').

    Raises:
        TypeError: If the relevant ID attribute ('id_row' or 'id_partition') in the model is neither a list nor a single value.

    Note:
        - The function dynamically determines the type of the model (scoring or feature engineering) based on the presence of specific attributes.
        - 'id_row' or 'id_partition' is converted to a list if it is not already one.
        - This function assumes the model is correctly instantiated and the necessary attributes are properly defined.

    Example:
        model = <instance of tdstone2 model>
        entity_id_types = tdstone2_entity_id(model)
        # entity_id_types might look like {'ID': 'BIGINT'}
    """

    # Initialize an empty dictionary to store entity IDs and their data types.
    entity_id = {}

    # Retrieve the list of IDs from the 'id_row' attribute of 'mapper_scoring' in the model.
    if 'score' in [x[0] for x in inspect.getmembers(type(existing_model))]:
        ids = existing_model.mapper_scoring.id_row
        model_type = 'model scoring'
    elif existing_model.feature_engineering_type == 'feature engineering reducer':
        ids = existing_model.mapper.id_partition
        model_type = 'feature engineering'
    else:
        ids = existing_model.mapper.id_row
        model_type = 'feature engineering'

    # Ensure 'ids' is a list. If not, convert it into a list.
    if type(ids) != list:
        ids = [ids]

    # Iterate over each ID in 'ids' and map it to its corresponding data type in the dictionary.
    if model_type == 'model scoring':
        for k in ids:
            entity_id[k] = existing_model.mapper_scoring.types[k]
    else:
        for k in ids:
            entity_id[k] = existing_model.mapper.types[k]

    # Return the dictionary containing mappings of entity IDs to data types.
    return entity_id

def remove_entity(entity, data_domain=None):
    """
    Removes all database entities (tables and views) associated with a given entity name within a specific data domain,
    and then removes the entity's metadata from the feature catalog.

    This function first constructs a SQL query to select distinct table and view names associated with the given entity
    name and data domain from the feature catalog. It then iterates over the list of tables and views, attempting to drop
    each one. Progress and status of these operations are tracked using a progress bar. If an error occurs during the drop
    operation, the error message is displayed in the progress bar description. Finally, the function constructs and executes
    another SQL query to delete the entity's metadata from the feature catalog.

    Parameters:
    - entity (str): The name of the entity to be removed.
    - data_domain (str, optional): The data domain where the entity is located. If not provided,
      the default data domain from `tdfs4ds.DATA_DOMAIN` is used.

    The function utilizes the `tdfs4ds.DEBUG_MODE` flag to control the printing of SQL queries for debugging purposes. If
    DEBUG_MODE is set to True, the queries for selecting and deleting entities are printed to the console.

    Dependencies:
    - Requires the `tdfs4ds` module for configuration constants like `DATA_DOMAIN`, `SCHEMA`, and `FEATURE_CATALOG_NAME`,
      as well as the `DEBUG_MODE` flag.
    - Requires the `tdml` module or object with an `execute_sql` method for database operations.
    - Uses the `tqdm` module to display a progress bar for the operations.

    Note:
    - This function assumes that the necessary permissions are in place for dropping tables and views, as well as deleting
      metadata entries from the feature catalog.
    - Exception handling within the dropping operations is limited to displaying the first line of any encountered error
      messages in the progress bar description. Further error handling or cleanup may be necessary depending on the
      specific requirements and database configuration.

    Returns:
    - None. The primary effect of this function is to alter the state of the database by removing entities and their
      metadata, not to return data to the caller.
    """
    if data_domain is None:
        data_domain = tdfs4ds.DATA_DOMAIN

    if type(entity) == list:
        entity.sort()
        entity_ = ','.join(entity)
    else:
        entity_ = entity

    query = f"""
    SELECT DISTINCT
        FEATURE_DATABASE || '.' || FEATURE_TABLE AS TABLE_NAME,
        FEATURE_DATABASE || '.' || FEATURE_VIEW  AS VIEW_NAME
    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME}
    WHERE DATA_DOMAIN = '{data_domain}'
    AND ENTITY_NAME = '{entity_}'
    """
    if tdfs4ds.DEBUG_MODE:
        print(query)

    list_to_drop = tdml.execute_sql(query).fetchall()

    pbar = tqdm.tqdm(list_to_drop, desc="Starting")
    for row in pbar:
        pbar.set_description(f"DROP VIEW {row[1]}")
        try:
            tdml.execute_sql(f'DROP VIEW  {row[1]}')
        except Exception as e:
            pbar.set_description(str(e).split('\n')[0])
        pbar.set_description(f"DROP TABLE {row[0]}")
        try:
            tdml.execute_sql(f'DROP TABLE {row[0]}')
        except Exception as e:
            pbar.set_description(str(e).split('\n')[0])

    query = f"""
    NONSEQUENCED VALIDTIME DELETE {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME}
    WHERE ENTITY_NAME = '{entity_}'
    AND DATA_DOMAIN = '{data_domain}'
    """
    if tdfs4ds.DEBUG_MODE:
        print(query)

    tdml.execute_sql(query)

    return