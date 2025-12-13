import re
import pandas as pd
import teradataml as tdml
import tdfs4ds
import tqdm
import networkx as nx
import sqlparse


def query_change_case(query, case):
    """
    Change the case of alternate segments of a query string split by single quotes.

    Parameters:
    query (str): The input query string to be processed.
    case (str): The case to change the segments to. Should be 'lower' or 'upper'.

    Returns:
    str: The query string with alternate segments in the specified case.

    Raises:
    ValueError: If 'case' is not 'lower' or 'upper'.
    """
    # Split the query string by single quotes
    splitted_query = query.split("'")

    # Check the case parameter and apply the case change accordingly
    if case == 'lower':
        # Convert every alternate segment to lowercase
        splitted_query = [c.lower() if i % 2 == 0 else c for i, c in enumerate(splitted_query)]
    elif case == 'upper':
        # Convert every alternate segment to uppercase
        splitted_query = [c.upper() if i % 2 == 0 else c for i, c in enumerate(splitted_query)]
    else:
        # Raise an error if the case parameter is invalid
        raise ValueError("Invalid case argument. Use 'lower' or 'upper'.")

    # Join the segments back together with single quotes and return the result
    return "'".join(splitted_query)

def query_replace(query, word, substitute):
    """
    Replace occurrences of a specific word in alternating segments of a query string, delimited by single quotes.

    Parameters:
    query (str): The input query string to be processed.
    word (str): The word to be replaced within the segments.
    substitute (str): The word to substitute in place of the 'word' parameter.

    Returns:
    str: The query string with occurrences of 'word' replaced by 'substitute' in alternating segments.

    Raises:
    ValueError: If either 'query', 'word', or 'substitute' is not a string.
    """

    # Split the query string by single quotes
    splitted_query = query.split("'")

    # Replace the word in alternate segments
    splitted_query = [c.replace(word, substitute) if i % 2 == 0 else c for i, c in enumerate(splitted_query)]

    # Join the segments back together with single quotes and return the result
    return "'".join(splitted_query)


def _analyze_sql_query(sql_query):
    """
    Analyzes a SQL query and extracts table and view names categorized as 'source' and 'target'.

    This function takes a SQL query as input, removes comments from the query, and then identifies
    tables and views mentioned in various SQL components such as CREATE TABLE, INSERT INTO, CREATE VIEW,
    and SELECT statements. The identified table and view names are categorized into 'source' and 'target',
    representing the tables/views that are being referenced and the ones that are being created or inserted into.

    Args:
        sql_query (str): The SQL query to be analyzed.

    Returns:
        dict: A dictionary containing two lists - 'source' and 'target', where 'source' contains the
        table and view names being referenced in the query, and 'target' contains the table and view names
        being created or inserted into in the query. The names are normalized with double quotes for
        consistency and may include schema references.
    """

    def find_in_with_statement(sql_text):
        """
        Extracts terms from a SQL text that are followed by 'AS ('.

        Args:
            sql_text (str): The SQL text to be searched.

        Returns:
            list: A list of terms that are followed by 'AS ('
        """
        # Regex pattern to find ', term AS ('
        # It looks for a comma, optional whitespace, captures a word (term), followed by optional whitespace, 'AS', whitespace, and an opening parenthesis
        pattern = r'WITH\s*(\w+)\s+AS\s+\('

        # Find all occurrences of the pattern
        terms = re.findall(pattern, sql_text, re.IGNORECASE)

        pattern = r',\s*(\w+)\s+AS\s+\('

        # Find all occurrences of the pattern
        terms = terms + re.findall(pattern, sql_text, re.IGNORECASE)

        terms = [t.split(' ')[0] for t in terms]
        return terms

    def remove_sql_comments(sql_query):
        # Remove single line comments
        sql_query = re.sub(r'--.*', '', sql_query)

        # Remove multi-line comments
        sql_query = re.sub(r'/\*.*?\*/', '', sql_query, flags=re.DOTALL)

        return sql_query

    # we remove the comments from the query
    sql_query = remove_sql_comments(sql_query)

    # Regular expression patterns for different SQL components
    create_table_pattern = r'CREATE\s+TABLE\s+([\w\s\.\"]+?)\s+AS'
    insert_into_pattern = r'INSERT\s+INTO\s+([\w\s\.\"]+?)'
    create_view_pattern = r'(CREATE|REPLACE)\s+VIEW\s+([\w\s\.\"]+?)\s+AS'
    #select_pattern = r'(FROM|JOIN|LEFT\sJOIN|RIGHT\sJOIN)\s+([\w\s\.\"]+?)(?=\s*(,|\s+GROUP|$|WHERE|PIVOT|UNPIVOT|UNION|ON|\)|\s+AS))'
    select_pattern = r'(\bFROM\b|LEFT\s+JOIN|RIGHT\s+JOIN|\bJOIN\b)\s+([\w\s\.\"]+?)(?=\s*(,|\bUNION\b|\bFULL\b|\bJOIN\b|\bLEFT\b|\bRIGHT\b|\bGROUP\b|\bQUALIFY\b|\bQUALIFY\b|\bWHERE\b|\bPIVOT\b|\bUNPIVOT\b|\bUNION\b|\bON\b|\bAS\b|$|\)))'
    select_pattern = r'(\bFROM\b|CROSS\s+JOIN|FULL\sOUTER\s+JOIN|LEFT\s+JOIN|RIGHT\s+JOIN|\bJOIN\b)\s+([\w\s\.\"]+?)(?=\s*(,|\bUNION\b|\bFULL\b|\bJOIN\b|\bLEFT\b|\bRIGHT\b|\bGROUP\s+BY\b|\bQUALIFY\b|\bHAVING\b|\bWHERE\b|\bPIVOT\b|\bUNPIVOT\b|\bUNION\b|\bUNION\s+ALL\b|\bINTERSECT\b|\bMINUS\b|\bEXCEPT\b|\bON\b|\bAS\b|$|\)))'
    select_pattern = r'(\bFROM\b|\bON\b|CROSS\s+JOIN|FULL\sOUTER\s+JOIN|INNER\s+JOIN|LEFT\s+JOIN|RIGHT\s+JOIN|\bJOIN\b)\s+([\w\s\.\"]+?)(?=\s*(,|\bUNION\b|\bINNER\b|\bCROSS\b|\bFULL\b|\bJOIN\b|\bLEFT\b|\bRIGHT\b|\bGROUP\s+BY\b|\bQUALIFY\b|\bHAVING\b|\bWHERE\b|\bPIVOT\b|\bUNPIVOT\b|\bUNION\b|\bUNION\s+ALL\b|\bINTERSECT\b|\bMINUS\b|\bEXCEPT\b|\bON\b|\bAS\b|$|\)))'

    # select_pattern2 =  r'(FROM|JOIN)\s+([\w\s\.\"]+?)(?=\s*(,|group|$|where|pivot|unpivot|\)|AS))'



    # Find all matches in the SQL query for each pattern
    create_table_matches = re.findall(create_table_pattern, sql_query, re.IGNORECASE)
    insert_into_matches = re.findall(insert_into_pattern, sql_query, re.IGNORECASE)
    create_view_matches = re.findall(create_view_pattern, sql_query, re.IGNORECASE)
    select_matches = re.findall(select_pattern, sql_query, re.IGNORECASE)

    # select_matches2 = re.findall(select_pattern2, sql_query, re.IGNORECASE)

    # Extract the actual table or view name from the match tuples
    create_table_matches = [match[0] if match[0] else match[1] for match in create_table_matches]
    insert_into_matches = [match[0] if match[0] else match[1] for match in insert_into_matches]
    create_view_matches = [match[1] if match[0] else match[1] for match in create_view_matches]
    if tdfs4ds.DEBUG_MODE:
        print('select matches :', select_matches)
    with_matches = [x.lower() for x in find_in_with_statement(sql_query)]
    select_matches = [match[1] for match in select_matches]
    if tdfs4ds.DEBUG_MODE:
        print('select matches :', select_matches)
    # select_matches2 = [match[0] for match in select_matches2]

    table_names = {
        'source': [],
        'target': []
    }

    # Categorize the matched tables and views into 'source' or 'target'
    table_names['target'].extend(create_table_matches)
    table_names['target'].extend(insert_into_matches)
    table_names['target'].extend(create_view_matches)
    table_names['source'].extend(select_matches)
    # table_names['source'].extend(select_matches2)

    # Remove duplicate table and view names
    table_names['source'] = list(set(table_names['source']))
    table_names['target'] = list(set(table_names['target']))

    correct_source = []
    for target in table_names['source']:
        if '"' not in target:
            if ' ' in target:
                target = target.split(' ')[0]
            if target.lower() not in with_matches:
                correct_source.append('.'.join(['"' + t + '"' for t in target.split('.')]))
        else:
            if target.lower() not in with_matches:
                correct_source.append(target)

    correct_target = []
    for target in table_names['target']:
        if '"' not in target:
            if ' ' in target:
                target = target.split(' ')[0]
            if target.lower() not in with_matches:
                correct_target.append('.'.join(['"' + t + '"' for t in target.split('.')]))
        else:
            if target.lower() not in with_matches:
                correct_target.append(target)

    table_names['source'] = [c.split(' ')[0] for c in correct_source]
    table_names['target'] = [c.split(' ')[0] for c in correct_target]



    return table_names

def analyze_sql_query(sql_query, df=None, target=None, root_name='ml__', node_info=None):
    """
    Analyzes a SQL query and its relationships to target tables/views.

    This function takes a SQL query as input and extracts source tables/views mentioned in the query.
    It also allows for recursively analyzing TeradataML (tdml) views to identify relationships and dependencies
    between the source tables/views and target tables/views. The analysis results are accumulated in a TeradataML
    DataFrame (df) and a list of node information (node_info) to capture target, columns, and query details.

    Args:
        sql_query (str): The SQL query to be analyzed.
        df (teradataml.DataFrame, optional): An existing TeradataML DataFrame to append the analysis results to.
            Default is None.
        target (str, optional): The target table/view where the query is directed. Default is None.
        root_name (str, optional): A root name identifier for filtering TeradataML views. Default is 'ml__'.
        node_info (list, optional): A list of dictionaries containing node information. Default is None.

    Returns:
        tuple: A tuple containing the analysis results - a TeradataML DataFrame (df) containing source and target
        table/view relationships, and a list of node information (node_info) capturing details about each node
        in the analysis.

    Note:
        - The 'target' parameter should be specified when analyzing queries directed at a specific table/view.
        - When analyzing TeradataML views, the function recursively extracts and analyzes the view's definition.

    Example:
        To analyze a SQL query:
        >>> result_df, result_node_info = analyze_sql_query(sql_query)

        To analyze a SQL query with a specific target table/view:
        >>> result_df, result_node_info = analyze_sql_query(sql_query, target='my_target_table')

        To analyze a SQL query and append results to an existing TeradataML DataFrame:
        >>> existing_df = teradataml.DataFrame()
        >>> result_df, result_node_info = analyze_sql_query(sql_query, df=existing_df)

    """

    # Extract source and potential target tables/views from the provided SQL query
    table_name = _analyze_sql_query(sql_query)


    # Extract node informations
    if node_info is None and target is None:
        node_info = [{'target': target, 'columns': tdml.DataFrame.from_query(sql_query).columns, 'query': sql_query}]
    elif node_info is None:
        if '"' not in target:
            target = '.'.join(['"' + t + '"' for t in target.split('.')])

        node_info = [{'target': target, 'columns': tdml.DataFrame(target).columns, 'query': sql_query}]
    else:
        if '"' not in target:
            target = '.'.join(['"' + t + '"' for t in target.split('.')])

        node_info = node_info + [{'target': target, 'columns': tdml.DataFrame(target).columns, 'query': sql_query}]

    # If df is not provided, initialize it; else append to the existing df
    table_name['target'] = [target] * len(table_name['source'])
    if df is None:
        df = pd.DataFrame(table_name)
    else:
        df = pd.concat([df, pd.DataFrame(table_name)], ignore_index=True)

    # Check for teradataml views in the source and recursively analyze them
    for obj in table_name['source']:
        print(obj)
        if root_name == None or root_name.lower() in obj.lower():

            # It's a teradataml view. Fetch its definition.
            try:
                sql_query_ = tdml.execute_sql(f"SHOW VIEW {obj}").fetchall()[0][0].replace('\r', '\n').replace('\t', '\n')
            except Exception as e:
                if tdfs4ds.DISPLAY_LOGS:
                    print(str(e).split("\n")[0])
            try:
                # Recursively analyze the view definition to get its relationships
                df, node_info = analyze_sql_query(
                    sql_query_,
                    df,
                    target    = obj,
                    node_info = node_info,
                    root_name = root_name
                )

                if tdfs4ds.DEBUG_MODE:
                    print('-------------------------------------------')
                    print('source     : ', obj)
                    print('-------------------------------------------')
                    print('source DDL : ')
                    print(sql_query_)
                    print('-------------------------------------------')
                    print(node_info)

            except:
                if tdfs4ds.DISPLAY_LOGS:
                    print(f"{obj} is a root, outside of the current database or a view directly connected to a table")

        else:
            if tdfs4ds.DISPLAY_LOGS:
                print(root_name.lower(), ' not in ', obj.lower(), 'then excluded', '(root_name :',root_name,')')

    return df, node_info


def crystallize_view(tddf, view_name, schema_name, output_view=True):
    """
    Crystallizes a TeradataML DataFrame into a database view.

    This function takes a TeradataML DataFrame (`tddf`) and converts its SQL representation into a database view.
    It analyzes dependencies, creates sub-views if needed, and constructs the final view with the specified
    `view_name` and `schema_name`. The resulting view can optionally be returned as a TeradataML DataFrame.

    Args:
        tddf (teradataml.DataFrame): The TeradataML DataFrame to be converted into a view.
        view_name (str): The name of the main view to be created or replaced in the database.
        schema_name (str): The schema where the view will be created.
        output_view (bool, optional): If `True`, returns a TeradataML DataFrame representing the created view.
                                      If `False`, the function performs the operation without returning a DataFrame.
                                      Default is `True`.

    Returns:
        teradataml.DataFrame: A TeradataML DataFrame representation of the created or replaced view,
                              if `output_view` is `True`. Otherwise, returns `None`.

    Raises:
        Exception: If there is an error during SQL execution for creating sub-views or the main view.

    Notes:
        - The `tddf` parameter must be a valid TeradataML DataFrame.
        - The function generates a dependency graph for the SQL query representing the input DataFrame.
          Sub-views are created or replaced with new names based on this graph.
        - Column names are replaced case-insensitively to ensure consistency in SQL queries.
        - The function replaces "CREATE VIEW" with "REPLACE VIEW" to handle updates.

    Example:
        To crystallize a TeradataML DataFrame into a view:

        >>> result_df = crystallize_view(my_teradataml_df, 'my_view', 'my_schema')

    """

    from collections import OrderedDict

    tddf_columns = tddf.columns

    # Function to replace column names in the query with case-insensitive matching
    def replace_case_insensitive(query, old_name, new_name):
        pattern = r'\b' + re.escape(old_name) + r'\b'
        return re.sub(pattern, new_name, query, flags=re.IGNORECASE)

    # Create the _table_name attribute for the teradataml DataFrame if it doesn't exist
    tddf._DataFrame__execute_node_and_set_table_name(tddf._nodeid, tddf._metaexpr)

    # Generate the dependency graph for the input DataFrame's SQL representation
    tddf_graph_, _ = analyze_sql_query(tddf.show_query(), target=tddf._table_name)


    # here we remove edge linking the same object to itself
    tddf_graph = []
    for i,row in tddf_graph_.iterrows():
        if not row['source'] == row['target']:
            tddf_graph.append([row['source'], row['target']])
    tddf_graph = pd.DataFrame(tddf_graph, columns=['source','target'])

    # Create a directed graph using networkx for dependency management
    dependency_graph = nx.DiGraph()

    # Add edges to the dependency graph
    print('source','target')
    for parent, child in zip(tddf_graph['source'].values, tddf_graph['target'].values):
        dependency_graph.add_edge(parent, child)
        print(parent, child)

    # Perform a topological sort to get the correct creation order
    sorted_nodes = list(nx.topological_sort(dependency_graph))
    
    # Select the targets in the sorted_nodes orders that are a temporary dataframe:
    targets_ = [x for x in sorted_nodes if len(x.split('.'))>1 and (
                x.split('.')[1].upper().startswith('ML__') or x.split('.')[1].upper().startswith('"ML__'))]

    targets = []
    for v in targets_:
        if v not in targets:
            targets.append(v)

    # print('sorted_nodes', sorted_nodes)
    # print('targets_',targets_)
    # print('targets',targets)

    # Generate new names for sub-views based on the main view's name and store in a mapping dictionary
    print('temporary views to rename (in that order):')
    if len(targets) > 1:
        mapping = OrderedDict({n: schema_name + '.' + view_name + '_sub_' + str(i) for i, n in enumerate(targets)})
        for i, v in enumerate(targets):
            print('- ', v, '=>', mapping[v])
    else:
        if len(targets)==1:
            mapping = {tddf_graph['target'].values[0]: schema_name + '.' + view_name}
            print('- ', tddf_graph['target'].values[0], '=>', schema_name + '.' + view_name)
        else:
            mapping = {tddf._table_name:  schema_name + '.' + view_name}
            print('- ', tddf._table_name, '=>', schema_name + '.' + view_name)

    # Replace or create the sub-views with their new names in the database
    for old_name, new_name in mapping.items():
        query = query_change_case(tdml.execute_sql(f"SHOW VIEW {old_name}").fetchall()[0][0].replace('\r', '\n'),
                                  'lower')
        query = query_replace(query, 'create', 'replace')
        for old_sub_name, new_sub_name in mapping.items():
            query = query_change_case(query, 'upper').replace(old_sub_name.upper(), new_sub_name)
            query = query.replace(f'REPLACE VIEW {new_sub_name.upper()} AS',
                                  f'REPLACE VIEW {new_sub_name.upper()} AS LOCK ROW FOR ACCESS')
        if tdfs4ds.DEBUG_MODE:
            print('------------------')
            print(query)
        for col in tddf_columns:
            query = replace_case_insensitive(query, col, col)  # replacing column names to ensure correct case
        try:
            tdml.execute_sql(query)
        except Exception as e:
            print("Error executing SQL query:", e)
            print("Query:", query)
            raise e from None

    # Construct the final view by replacing the old names with new ones in the SQL representation
    mapping[new_name] = schema_name + '.' + view_name
    print('- ', new_name, '=>', schema_name + '.' + view_name)
    # query = tdml.execute_sql(f"SHOW VIEW {tddf._table_name}").fetchall()[0][0].replace('\r','\n').lower()
    # query = f'replace view {schema_name}.{view_name} AS \n' + query
    for old_name, new_name in mapping.items():
        query = query_change_case(query, 'upper').replace(old_name.upper(), new_name)
        # query = query.replace(f'REPLACE VIEW {new_sub_name.upper()} AS',
        #                      f'REPLACE VIEW {new_sub_name.upper()} AS LOCK ROW FOR ACCESS')
    for col in tddf_columns:
        query = replace_case_insensitive(query, col, col)  # replacing column names to ensure correct case

    # Execute the final query to create the main view
    if tdfs4ds.DISPLAY_LOGS:
        print('REPLACE VIEW ' + schema_name + '.' + view_name)
    if tdfs4ds.DEBUG_MODE:
        print('------------------')
        print(query)
    try:
        tdml.execute_sql(query)
    except Exception as e:
        print("Error executing SQL query:", e)
        print("Query:", query)
        raise e from None

    if output_view:
        # Return a teradataml DataFrame representation of the created view
        return tdml.DataFrame(tdml.in_schema(schema_name, view_name))
    else:
        return

def generate_view_dependency_network(schema_name):
    """
        Generates a dependency network of views within a specified schema.

        This function lists all views within the given schema, analyzes their SQL queries to identify dependencies,
        and constructs a dependency network represented as a pandas DataFrame. The DataFrame contains source and target
        view relationships, capturing how views in the schema are interconnected.

        Args:
            schema_name (str): The name of the schema containing the views for which the dependency network is generated.

        Returns:
            pandas.DataFrame: A DataFrame representing the view dependency network with source and target view relationships.

        Note:
            - The 'schema_name' parameter should specify the name of the schema containing the views to be analyzed.
            - The resulting DataFrame shows how views in the schema depend on each other.

        Example:
            To generate a view dependency network for a schema:
            >>> dependency_df = generate_view_dependency_network('my_schema')

        """

    # Temporarily disable logging to prevent clutter during the process
    display_logs = tdfs4ds.DISPLAY_LOGS
    tdfs4ds.DISPLAY_LOGS = False

    try:
        # List all views in the given schema
        views = tdml.db_list_tables(schema_name=schema_name, object_type='view').TableName.tolist()

        # Initialize an empty list to store dataframes representing individual view dependencies
        df_list = []

        # Initialize a progress bar for processing views
        pbar = tqdm.tqdm(views, desc="Starting")
        for v in pbar:
            pbar.set_description(f"Processing view {v}")

            # Analyze the SQL query for the current view and retrieve a dataframe representing its dependencies
            df, node_info = analyze_sql_query(get_ddl(view_name=v, schema_name=schema_name), target=f"{schema_name}.{v}", root_name=None)

            # Append the resulting dataframe to the list
            df_list.append(df)

        # Concatenate all individual view dependency dataframes and remove duplicates
        combined_df = pd.concat(df_list).drop_duplicates()

        # Restore the original logging setting
        tdfs4ds.DISPLAY_LOGS = display_logs

        return combined_df

    except Exception as e:
        # In case of an exception, restore logging settings and print the error
        tdfs4ds.DISPLAY_LOGS = display_logs
        print(str(e))
        return None


def generate_view_dependency_network_fs(schema_name):
    """
    Generates a dependency network between views and features within a specified schema.

    This function constructs a dependency network by analyzing relationships between views and features
    within the given schema. It performs a SQL query to identify dependencies and creates a pandas DataFrame
    representing the relationships between views (source) and features (target).

    Args:
        schema_name (str): The name of the schema containing the views and features for which the dependency
        network is generated.

    Returns:
        pandas.DataFrame: A DataFrame representing the dependency network between views (source) and features (target).

    Note:
        - The 'schema_name' parameter should specify the name of the schema containing the relevant views and features.
        - The resulting DataFrame shows how views within the schema depend on specific features.

    Example:
        To generate a view-feature dependency network for a schema:
        >>> dependency_df = generate_view_dependency_network_fs('my_schema')

    """

    try:
        # Construct the pattern for matching view names in the schema
        pattern = '"' + schema_name + '".%'

        # SQL query to find dependencies between views and features
        query = f"""
        WITH SELECTED_PROCESS AS (
            SELECT * FROM NGramSplitter(
                ON (
                    CURRENT VALIDTIME
                    SELECT 
                        VIEW_NAME,
                        FEATURE_NAMES,
                        DATA_DOMAIN
                    FROM {tdfs4ds.SCHEMA}.{tdfs4ds.PROCESS_CATALOG_NAME}
                    WHERE VIEW_NAME LIKE '{pattern}'
                ) AS "input"
                PARTITION BY ANY
                USING
                TextColumn('FEATURE_NAMES')
                Grams('1')
                Delimiter(',')
                NGramColName('FEATURE_NAME')
            ) as sqlmr
        )
        SELECT DISTINCT
            A.VIEW_NAME AS source,
            '"'||B.FEATURE_DATABASE||'"."'||B.FEATURE_TABLE||'"' AS target
        FROM SELECTED_PROCESS AS A
        INNER JOIN (CURRENT VALIDTIME SEL * FROM {tdfs4ds.SCHEMA}.{tdfs4ds.FEATURE_CATALOG_NAME}) AS B
        ON A.DATA_DOMAIN = B.DATA_DOMAIN AND A.FEATURE_NAME = B.FEATURE_NAME"""

        # Execute the query and convert the result to a pandas DataFrame
        graph = tdml.DataFrame.from_query(query).to_pandas()

        return graph

    except Exception as e:
        # Print the first line of the exception message and return None
        print(str(e).split('\n')[0])
        print(query)
        return None



def get_ddl(view_name, schema_name, object_type='view'):
    """
    Retrieves the Data Definition Language (DDL) for a view or table in a specified schema.

    This function allows you to retrieve the DDL for a view or table within a specific schema. You can specify
    the object type ('view' or 'table') to determine whether to retrieve the DDL for a view or a table.

    Args:
        view_name (str): The name of the view or table for which to retrieve the DDL.
        schema_name (str): The name of the schema containing the view or table.
        object_type (str, optional): The type of the object ('view' or 'table') for which to retrieve the DDL.
            Default is 'view'.

    Returns:
        str: The DDL (Data Definition Language) statement for the specified view or table.

    Raises:
        ValueError: If the 'object_type' parameter is not recognized or is not 'view' or 'table'.

    Note:
        - The 'view_name' parameter should specify the name of the view or table.
        - The 'schema_name' parameter should specify the name of the schema containing the view or table.

    Example:
        To retrieve the DDL for a view:
        >>> ddl_statement = get_ddl('my_view', 'my_schema', object_type='view')

        To retrieve the DDL for a table:
        >>> ddl_statement = get_ddl('my_table', 'my_schema', object_type='table')

    """

    # Execute the appropriate SQL command based on the object type
    if object_type == 'view':
        # Retrieve DDL for a view
        ddl = tdml.execute_sql(f'SHOW VIEW {schema_name}.{view_name}').fetchall()[0][0]
    elif object_type == 'table':
        # Retrieve DDL for a table
        ddl = tdml.execute_sql(f'SHOW TABLE {schema_name}.{view_name}').fetchall()[0][0]
    else:
        # Raise an error if the object_type is not recognized
        raise ValueError("Invalid object_type. Authorized values are 'view' and 'table'")

    # Replace carriage returns with newlines for consistent formatting
    return ddl.replace('\r', '\n')

import os
import datetime
import sqlparse
import tdfs4ds
import importlib.resources as pkg_resources  


def generate_process_report(
    format="html",
    output_file=None,
    collapsible=False,
    sort_by="view_name",
    theme_mode="light",
    company_name=None,
    company_logo_url=None
):
    """
    Generate a process catalog report styled after the Teradata website.
    """

    # Retrieve processes
    processes = tdfs4ds.process_catalog()
    processes = processes[processes.DATA_DOMAIN == tdfs4ds.DATA_DOMAIN].to_pandas()
    processes['VIEW'] = processes['VIEW_NAME'].apply(lambda x: x.split('.')[1].replace('"', ""))

    def split_view_name(full_name):
        db, vw = full_name.replace('"', '').split('.')
        return db, vw

    if sort_by:
        processes = processes.copy()
        processes["DB"], processes["VW"] = zip(*processes["VIEW_NAME"].map(split_view_name))
        if sort_by == "database":
            processes = processes.sort_values(["DB", "VW"])
        elif sort_by == "view_name":
            processes = processes.sort_values(["VW"])
        elif sort_by == "database,view_name":
            processes = processes.sort_values(["DB", "VW"])

    # Timestamp and output file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not output_file:
        output_file = f"process_report_{tdfs4ds.DATA_DOMAIN}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    # Theme
    if theme_mode == "dark":
        bg_color = "#121212"
        text_color = "#f5f5f5"
        sidebar_bg = "#1e1e1e"
        border_color = "#333"
        pre_bg = "#222"
        teradata_logo_file = "teradata_sym_rgb_wht_rev.png"
    else:
        bg_color = "#ffffff"
        text_color = "#000000"
        sidebar_bg = "#f8f9fa"
        border_color = "#e1e1e1"
        pre_bg = "#f4f6f8"
        teradata_logo_file = "teradata_sym_rgb_pos.png"

    # Load Teradata logo
    with pkg_resources.path("tdfs4ds.data.logo", teradata_logo_file) as p:
        teradata_logo_path = str(p)
    with pkg_resources.path("tdfs4ds.data.logo", "tdfs4ds_logo.png") as p:  # ensure you add this logo to package
        tdfs4ds_logo_path = str(p)

    # HTML Report
    report_parts = []

    if format == "html":
        report_parts.append("<html><head>")
        report_parts.append("<meta charset='utf-8'>")
        report_parts.append("<title>Process Catalog Report</title>")
        report_parts.append(f"""
        <style>
        body {{
            font-family: "Segoe UI", Arial, sans-serif;
            margin: 0;
            display: flex;
            background: {bg_color};
            color: {text_color};
            height: 100vh;
            overflow: hidden;
        }}
        .sidebar {{
            width: 260px;
            background: {sidebar_bg};
            display: flex;
            flex-direction: column;
            border-right: 1px solid {border_color};
            box-shadow: 2px 0 8px rgba(0,0,0,0.05);
        }}
        .sidebar-header {{
            padding: 20px;
            text-align: center;
            border-bottom: 1px solid {border_color};
        }}
        .sidebar-header img {{
            height: 35px;
            max-width: 90%;
            margin: 10px 0;
        }}
        .sidebar-content {{
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }}
        .content-wrapper {{
            flex: 1;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }}
        .header {{
            flex: 0 0 auto;
            background: #007CBA;
            color: white;
            padding: 20px;
        }}
        .header h1 {{
            margin: 0 0 10px;
        }}
        .header p {{
            margin: 5px 0;
            font-size: 0.95em;
        }}
        .content {{
            flex: 1;
            padding: 30px;
            overflow-y: auto;
        }}
        .footer {{
            flex: 0 0 auto;
            padding: 15px;
            border-top: 1px solid {border_color};
            font-size: 0.9em;
            text-align: center;
            color: #666;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
        }}
        .footer img {{
            height: 25px;
        }}
        pre {{
            background: {pre_bg};
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 0.9em;
        }}
        ul {{ list-style-type: none; padding-left: 15px; }}
        a {{ text-decoration: none; color: #007CBA; }}
        a:hover {{ text-decoration: underline; }}
        h2, h3 {{ color: #007CBA; }}
        </style>
        """)
        report_parts.append("</head><body>")

        # Sidebar
        report_parts.append("<div class='sidebar'>")
        report_parts.append("<div class='sidebar-header'>")
        if company_logo_url:
            report_parts.append(f'<img src="{company_logo_url}" alt="Company logo"><br>')
        report_parts.append(f'<img src="{teradata_logo_path}" alt="Teradata logo">')
        report_parts.append("</div>")  # end sidebar-header

        # Sidebar content (index)
        report_parts.append("<div class='sidebar-content'>")
        report_parts.append("<h2>Process Catalog Index</h2><ul id='indexList'>")
        for db, db_group in processes.groupby("DB"):
            report_parts.append(f"<li><h3>DB: {db}</h3><ul>")
            for _, row in db_group.iterrows():
                view_id = f"{row['DB']}_{row['VW']}"
                report_parts.append(f'<li><a href="#{view_id}">{row["VW"]}</a><ul>')
                report_parts.append(f'<li><a href="#{view_id}_entity">Entity</a></li>')
                report_parts.append(f'<li><a href="#{view_id}_features">Features</a></li>')
                report_parts.append(f'<li><a href="#{view_id}_ddl">DDL</a></li>')
                report_parts.append("</ul></li>")
            report_parts.append("</ul></li>")
        report_parts.append("</ul></div></div>")  # close sidebar-content & sidebar

        # Main content wrapper
        report_parts.append("<div class='content-wrapper'>")

        # Header
        report_parts.append("<div class='header'>")
        report_parts.append("<h1>Process Catalog Report</h1>")
        report_parts.append("<p>Data Domain: Customer Transaction Analytics Time Management | "
                            f"Generated on {timestamp}</p>")
        report_parts.append("<p>Powered by <strong>Teradata</strong> and <strong>tdfs4ds</strong></p>")
        report_parts.append("</div>")  # end header

        # Content
        report_parts.append("<div class='content'>")

    # Sections per process
    for _, row in processes.iterrows():
        view_name = row['VIEW_NAME']
        db, vw = split_view_name(view_name)
        view_id = f"{db}_{vw}"
        entity_list = row['ENTITY_ID'].split(',')
        features_list = row['FEATURE_NAMES'].split(',')
        process_id = row['PROCESS_ID']
        ddl_raw = tdfs4ds.tdml.execute_sql(f"SHOW VIEW {view_name}").fetchall()[0][0]
        ddl = sqlparse.format(ddl_raw, reindent=True, keyword_case="upper")

        if format == "html":
            section = [f'<h2 id="{view_id}">{view_name}</h2>']
            section.append(f"<p><strong>PROCESS_ID:</strong> {process_id}</p>")
            section.append(f'<h3 id="{view_id}_entity">Entity</h3><ul>')
            section.extend([f"<li>{t}</li>" for t in entity_list])
            section.append("</ul>")
            section.append(f'<h3 id="{view_id}_features">Features ({len(features_list)} total)</h3><ul>')
            section.extend([f"<li>{t}</li>" for t in features_list])
            section.append("</ul>")
            section.append(f'<h3 id="{view_id}_ddl">DDL</h3>')

            if collapsible:
                section.append("<details><summary>Show/Hide DDL</summary><pre><code>")
                section.append(ddl)
                section.append("</code></pre></details>")
            else:
                section.append(f"<pre><code>{ddl}</code></pre>")

            report_parts.append("\n".join(section))

    if format == "html":
        report_parts.append("</div>")  # end content
        report_parts.append(
            f"<div class='footer'>"
            f'<a href="https://www.teradata.com" target="_blank">'
            f'<img src="{teradata_logo_path}" alt="Teradata logo"></a>'
            f'<a href="https://pypi.org/project/tdfs4ds/" target="_blank">'
            f'<img src="{tdfs4ds_logo_path}" alt="tdfs4ds logo"></a>'
            f"<span>© 2025 . Generated using tdfs4ds on Teradata.</span>"
            f"</div>"
        )
        report_parts.append("</div></body></html>")

    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_parts))

    return output_file
