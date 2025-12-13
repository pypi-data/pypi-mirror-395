import functools
import teradataml as tdml
import re
import pandas as pd
import sqlparse
import plotly.graph_objects as go
import os
from packaging import version
import datetime

def is_version_greater_than(tested_version, base_version="17.20.00.03"):
    """
    Check if the tested version is greater than the base version.

    Args:
        tested_version (str): Version number to be tested.
        base_version (str, optional): Base version number to compare. Defaults to "17.20.00.03".

    Returns:
        bool: True if tested version is greater, False otherwise.
    """
    return version.parse(tested_version) > version.parse(base_version)
def execute_query_wrapper(f):
    """
    Decorator to execute a query. It wraps around the function and adds exception handling.

    Args:
        f (function): Function to be decorated.

    Returns:
        function: Decorated function.
    """
    @functools.wraps(f)
    def wrapped_f(*args, **kwargs):
        query = f(*args, **kwargs)
        if is_version_greater_than(tdml.__version__, base_version="17.20.00.03"):
            if type(query) == list:
                for q in query:
                    try:
                        tdml.execute_sql(q)
                    except Exception as e:
                        print(str(e).split('\n')[0])
                        print(q)
            else:
                try:
                    tdml.execute_sql(query)
                except Exception as e:
                    print(str(e).split('\n')[0])
                    print(query)
        else:
            if type(query) == list:
                for q in query:
                    try:
                        tdml.get_context().execute(q)
                    except Exception as e:
                        print(str(e).split('\n')[0])
                        print(q)
            else:
                try:
                    tdml.get_context().execute(query)
                except Exception as e:
                    print(str(e).split('\n')[0])
                    print(query)
        return

    return wrapped_f


def execute_query(query):
    if is_version_greater_than(tdml.__version__, base_version="17.20.00.03"):
        if type(query) == list:
            for q in query:
                try:
                    tdml.execute_sql(q)
                except Exception as e:
                    print(str(e).split('\n')[0])
                    print(q)
        else:
            try:
                return tdml.execute_sql(query)
            except Exception as e:
                print(str(e).split('\n')[0])
                print(query)
    else:
        if type(query) == list:
            for q in query:
                try:
                    tdml.get_context().execute(q)
                except Exception as e:
                    print(str(e).split('\n')[0])
                    print(q)
        else:
            try:
                return tdml.get_context().execute(query)
            except Exception as e:
                print(str(e).split('\n')[0])
                print(query)
    return


def _analyze_sql_query(sql_query):
    """
    Analyze a SQL query to extract the source tables, target tables, and views.

    The function uses regular expressions to search for patterns indicative
    of source tables, target tables, and views in the given SQL query.

    :param sql_query: str
        A string containing a SQL query to be analyzed.

    :return: dict
        A dictionary containing lists of source tables, target tables, and views.
        Format: {
            'source': [source_tables],
            'target': [target_tables]
        }
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

    # Regular expression patterns for different SQL components
    create_table_pattern = r'CREATE\s+TABLE\s+([\w\s\.\"]+?)\s+AS'
    insert_into_pattern = r'INSERT\s+INTO\s+([\w\s\.\"]+?)'
    create_view_pattern = r'(CREATE|REPLACE)\s+VIEW\s+([\w\s\.\"]+?)\s+AS'
    #select_pattern = r'(FROM|JOIN|LEFT\sJOIN|RIGHT\sJOIN)\s+([\w\s\.\"]+?)(?=\s*(,|\s+GROUP|$|WHERE|PIVOT|UNPIVOT|UNION|ON|\)|\s+AS))'
    select_pattern = r'(FROM|JOIN|LEFT\s+JOIN|RIGHT\s+JOIN)\s+([\w\s\.\"]+?)(?=\s*(,|\bGROUP\b|\bWHERE\b|\bPIVOT\b|\bUNPIVOT\b|\bUNION\b|\bON\b|\bAS\b|$|\)))'
    # select_pattern2 =  r'(FROM|JOIN)\s+([\w\s\.\"]+?)(?=\s*(,|group|$|where|pivot|unpivot|\)|AS))'

    # Find all matches in the SQL query for each pattern
    create_table_matches = re.findall(create_table_pattern, sql_query, re.IGNORECASE)
    insert_into_matches = re.findall(insert_into_pattern, sql_query, re.IGNORECASE)
    create_view_matches = re.findall(create_view_pattern, sql_query, re.IGNORECASE)
    select_matches = re.findall(select_pattern, sql_query, re.IGNORECASE)

    # select_matches2 = re.findall(select_pattern2, sql_query, re.IGNORECASE)
    # print(select_matches2)
    # Extract the actual table or view name from the match tuples
    create_table_matches = [match[0] if match[0] else match[1] for match in create_table_matches]
    insert_into_matches = [match[0] if match[0] else match[1] for match in insert_into_matches]
    create_view_matches = [match[1] if match[0] else match[1] for match in create_view_matches]

    with_matches = [x.lower() for x in find_in_with_statement(sql_query)]
    select_matches = [match[1] for match in select_matches]

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

    table_names['source'] = correct_source
    table_names['target'] = correct_target

    return table_names

def analyze_sql_query(sql_query, df=None, target=None, root_name='ml__', node_info=None):
    """
    Analyzes the provided SQL query to determine source and target tables/views relationships.
    It then captures these relationships in a pandas DataFrame.

    :param sql_query: str
        A string containing the SQL query to be analyzed.
    :param df: pd.DataFrame, optional
        An existing DataFrame to append the relationships to. If not provided, a new DataFrame is created.
    :param target: str, optional
        Name of the target table/view. If not provided, it's deduced from the SQL query.

    :return: pd.DataFrame
        A DataFrame with two columns: 'source' and 'target', representing the relationships.

    :Note: This function is specifically tailored for Teradata and makes use of teradataml (tdml) for certain operations.
    """

    # Extract source and potential target tables/views from the provided SQL query
    table_name = _analyze_sql_query(sql_query)
    # print(table_name)
    # print(sql_query)
    # print('-----')

    # Extract node informations
    if node_info is None and target is None:
        node_info = [{'target': target, 'columns': tdml.DataFrame.from_query(sql_query).columns, 'query': sql_query}]
    elif node_info is None:
        if '"' not in target:
            target = '.'.join(['"' + t + '"' for t in target.split('.')])
            #print(target)
        node_info = [{'target': target, 'columns': tdml.DataFrame(target).columns, 'query': sql_query}]
    else:
        if '"' not in target:
            target = '.'.join(['"' + t + '"' for t in target.split('.')])
            #print(target)
        node_info = node_info + [{'target': target, 'columns': tdml.DataFrame(target).columns, 'query': sql_query}]

    # If df is not provided, initialize it; else append to the existing df
    table_name['target'] = [target] * len(table_name['source'])
    if df is None:
        df = pd.DataFrame(table_name)
    else:
        df = pd.concat([df, pd.DataFrame(table_name)], ignore_index=True)

    # Check for teradataml views in the source and recursively analyze them
    for obj in table_name['source']:
        if root_name == None or root_name.lower() in obj.lower():
            #print(obj)
            # It's a teradataml view. Fetch its definition.
            try:
                sql_query_ = tdml.execute_sql(f"SHOW VIEW {obj}").fetchall()[0][0].replace('\r', '\n').replace('\t', '\n')
            except Exception as e:
                print(str(e).split("\n")[0])
            try:
                # Recursively analyze the view definition to get its relationships
                df, node_info = analyze_sql_query(sql_query_, df, target=obj, node_info=node_info, root_name=root_name)
            except:
                print(f"{obj} is a root, outside of the current database or a view directly connected to a table")

        else:
            print(root_name.lower(), ' not in ', obj.lower(), 'then excluded')

    return df, node_info
def plot_graph(tddf, root_name='ml__'):
    """
    Visualizes a given dataframe's source-target relationships using a Sankey diagram.

    :param df: pd.DataFrame
        The input dataframe should have two columns: 'source' and 'target'.
        Each row represents a relationship between a source and a target.

    :Note: This function makes use of Plotly's Sankey diagram representation for visualization.

    :return: None
        The function outputs the Sankey diagram and doesn't return anything.
    """

    tddf._DataFrame__execute_node_and_set_table_name(tddf._nodeid, tddf._metaexpr)

    df, node_info = analyze_sql_query(tddf.show_query(), df=None, target=tddf._table_name, root_name=root_name)

    if df['source'].values[0].lower() == df['target'].values[0].lower():
        df = df.iloc[1::, :]

    # Create a list of unique labels combining sources and targets from the dataframe
    labels = list(pd.concat([df['source'], df['target']]).unique())

    # Creating a mapping of node labels to additional information
    node_info_dict = pd.DataFrame(node_info).set_index('target').T.to_dict()

    # Create hovertext for each label using the node_info_map
    hovertexts = [
        f"Columns:<br> {','.join(node_info_dict[label]['columns'])}<br> Query: {sqlparse.format(node_info_dict[label]['query'], reindent=True, keyword_case='upper')}".replace(
            '\n', '<br>').replace('PARTITION BY', '<br>PARTITION BY').replace('USING', '<br>USING').replace(' ON',
                                                                                                            '<br>ON').replace(') ',')<br>').replace(')<br>AS',') AS').replace(', ',',<br>')

        if label in node_info_dict else '' for label in labels]

    # Use the length of 'columns' for the value (thickness) of each link
    values = df['source'].apply(lambda x: len(node_info_dict[x]['columns']) if x in node_info_dict else 1)

    # Convert source and target names to indices based on their position in the labels list
    source_indices = df['source'].apply(lambda x: labels.index(x))
    target_indices = df['target'].apply(lambda x: labels.index(x))

    # Construct the Sankey diagram with nodes (sources & targets) and links (relationships)
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,  # Space between the nodes
            thickness=20,  # Node thickness
            line=dict(color="black", width=0.5),  # Node border properties
            label=labels,  # Labels for nodes
            color="blue",  # Node color
            # hovertext=link_hovertexts  # set hover text for nodes
            customdata=hovertexts,
            hovertemplate=' %{customdata}<extra></extra>',
        ),
        link=dict(
            source=source_indices,  # Link sources
            target=target_indices,  # Link targets
            value=values  # [1] * len(df)  # Assuming equal "flow" for each link. Can be modified if needed.
        )
    )])

    # Customize the layout, such as setting the title and font size
    fig.update_layout(title_text="Hierarchical Data Visualization", font_size=10)

    # Display the Sankey diagram
    fig.show()

    return df
def crystallize_view(tddf, view_name, schema_name):
    """
    Materializes a given teradataml DataFrame as a view in the database with sub-views, if needed. This function
    helps in creating nested views, where complex views are broken down into simpler sub-views to simplify debugging
    and optimization. Each sub-view is named based on the main view's name with an additional suffix.

    Parameters:
    :param tddf: teradataml.DataFrame
        The teradataml dataframe whose view needs to be materialized.
    :param view_name: str
        The name of the main view to be created.
    :param schema_name: str
        The schema in which the view should be created.

    Returns:
    :return: teradataml.DataFrame
        A teradataml DataFrame representation of the created view.

    Notes:
    This function is specific to the teradataml library, and assumes the existence of certain attributes in the input DataFrame.
    """

    # Create the _table_name attribute for the teradataml DataFrame if it doesn't exist
    tddf._DataFrame__execute_node_and_set_table_name(tddf._nodeid, tddf._metaexpr)

    # Generate the dependency graph for the input DataFrame's SQL representation
    tddf_graph, _ = analyze_sql_query(tddf.show_query(), target=tddf._table_name)

    # Generate new names for sub-views based on the main view's name and store in a mapping dictionary
    if len(tddf_graph['target'].values)>1:
        mapping = {n: schema_name + '.' + view_name + '_sub_' + str(i) for i, n in enumerate(tddf_graph['target'].values)}
    else:
        mapping = {tddf_graph['target'].values[0] : schema_name + '.' + view_name}

    # Replace or create the sub-views with their new names in the database
    for old_name, new_name in reversed(mapping.items()):
        query = tdml.execute_sql(f"SHOW VIEW {old_name}").fetchall()[0][0].replace('\r','\n').lower()
        query = query.replace('create', 'replace')
        for old_sub_name, new_sub_name in mapping.items():
            query = query.upper().replace(old_sub_name.upper(), new_sub_name)
        #print(query)
        print('REPLACE VIEW ', new_name)
        tdml.execute_sql(query)

    # Construct the final view by replacing the old names with new ones in the SQL representation
    mapping[new_name] = view_name

    #query = tdml.execute_sql(f"SHOW VIEW {tddf._table_name}").fetchall()[0][0].replace('\r','\n').lower()
    #query = f'replace view {schema_name}.{view_name} AS \n' + query
    for old_name, new_name in mapping.items():
        query = query.upper().replace(old_name.upper(), new_name)

    # Execute the final query to create the main view
    #print(query)
    print('REPLACE VIEW ', schema_name,'.',view_name)
    tdml.execute_sql(query)


    # Return a teradataml DataFrame representation of the created view
    return tdml.DataFrame(tdml.in_schema(schema_name, view_name))

def display_table(df, max_widths=[25, 55, 10], header=["Feature Database", "Feature Table", "# rows"]):
    # Create a format string for each row
    row_format = " | ".join("{:<" + str(width) + "." + str(width) + "}" for width in max_widths)

    # Print the header
    print('\n')
    print(row_format.format(*header))
    print("-" * (sum(max_widths) + 2 * (len(max_widths) - 1)))  # Account for separators

    # Iterate over rows and print each one
    for _, row in df.iterrows():
        print(row_format.format(*[str(row[col]) for col in df.columns]))

    print('\n')
    return


def get_column_types(df, columns):
    if type(columns) != list:
        columns = [columns]

    col_type = {x[0]: x[1] for x in df._td_column_names_and_types if x[0] in columns}

    for k, v in col_type.items():
        if v == 'VARCHAR':
            temp = df._td_column_names_and_sqlalchemy_types[k.lower()]
            col_type[k] = f"{temp.compile()} CHARACTER SET {temp.charset}"
    return col_type


def get_column_types_simple(df, columns):
    if type(columns) != list:
        columns = [columns]

    col_type = {x[0]: x[1] for x in df._td_column_names_and_types if x[0] in columns}

    mapping = {'INTEGER': 'int',
               'BYTEINT': 'int',
               'BIGINT': 'int',
               'FLOAT': 'float'
               }

    for k, v in col_type.items():
        if v in mapping.keys():
            col_type[k] = mapping[v]

    return col_type


class TimeManager:
    """
    A class to manage time-related operations in a database table.

    Attributes:
        schema_name (str): Name of the schema in the database.
        table_name (str): Name of the table in the schema.
        data_type (str): Type of the date/time data, defaults to 'DATE'.
    """

    def __init__(self, table_name, schema_name, data_type='DATE'):
        """
        Initializes the TimeManager with a table name, schema name, and optionally a data type.

        If the table doesn't exist, it creates one with a BUSINESS_DATE column of the specified data type.

        Args:
            table_name (str): Name of the table.
            schema_name (str): Name of the schema.
            data_type (str, optional): Type of the date/time data. Defaults to 'DATE'.
        """
        self.schema_name = schema_name
        self.table_name = table_name
        if not self._exists():
            self.data_type = data_type
            self._create_table()
        else:
            df = tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))
            d_ = {x[0]: x[1] for x in df._td_column_names_and_types}
            self.data_type = d_['BUSINESS_DATE']

    def _create_table(self):
        """
        Creates a table in the database with a BUSINESS_DATE column.
        """
        query = f"""
        CREATE TABLE {self.schema_name}.{self.table_name}
        (
            BUSINESS_DATE {self.data_type}
        )
        """
        tdml.execute_sql(query)

        if 'date' in self.data_type.lower():
            query = f"""
            INSERT INTO {self.schema_name}.{self.table_name} VALUES (CURRENT_DATE)
            """
        else:
            query = f"""
            INSERT INTO {self.schema_name}.{self.table_name} VALUES (CURRENT_TIME)
            """
        tdml.execute_sql(query)

    def _exists(self):
        """
        Checks if the table exists in the database.

        Returns:
            bool: True if the table exists, False otherwise.
        """

        return len([x for x in tdml.db_list_tables(schema_name=self.schema_name).TableName.values if
                    x.lower().replace('"', '') == self.table_name.lower()]) > 0

    def _drop(self):
        """
        Drops the table if it exists.
        """
        # Drop the table if it exists
        if self._exists():
            tdml.db_drop_table(schema_name=self.schema_name, table_name=self.table_name)

    def update(self, new_time=None):
        """
        Updates the BUSINESS_DATE in the table.

        Args:
            new_time (str, optional): The new time to update. If None, current date or time is used depending on the data type.
        """
        if self._exists():
            if new_time is None and 'date' in self.data_type.lower():
                query = f"""
                UPDATE {self.schema_name}.{self.table_name}
                SET BUSINESS_DATE = CURRENT_DATE
                """
            elif new_time is None:
                query = f"""
                UPDATE {self.schema_name}.{self.table_name}
                SET BUSINESS_DATE = CURRENT_TIME
                """
            else:
                query = f"""
                UPDATE {self.schema_name}.{self.table_name}
                SET BUSINESS_DATE = {self.data_type} '{new_time}'
                """
            tdml.execute_sql(query)

    def display(self):
        """
        Displays the table.

        Returns:
            DataFrame: The table data as a DataFrame.
        """
        return tdml.DataFrame(tdml.in_schema(self.schema_name, self.table_name))

    def get_date_in_the_past(self):
        # '9999-01-01 00:00:00'
        date_obj = self.display().to_pandas().reset_index().iloc[0,0]

        if isinstance(date_obj, datetime.datetime):
            # print("temp is a datetime.datetime object")
            datetime_obj = date_obj
        elif isinstance(date_obj, datetime.date):
            # print("temp is a datetime.date object")
            # Convert date object to a datetime object at midnight (00:00:00)
            datetime_obj = datetime.datetime.combine(date_obj, datetime.time.min)
        else:
            print("temp is neither a datetime.date nor a datetime.datetime object")
            return

        # Convert datetime object to string
        output_string = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

        return output_string