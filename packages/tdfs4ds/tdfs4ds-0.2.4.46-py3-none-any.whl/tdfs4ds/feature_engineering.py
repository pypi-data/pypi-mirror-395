import teradataml as tdml

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
def materialize_view(tddf, view_name, schema_name):
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
    mapping = {n: schema_name + '.' + view_name + '_sub_' + str(i) for i, n in enumerate(tddf_graph['target'].values)}

    # Replace or create the sub-views with their new names in the database
    for old_name, new_name in reversed(mapping.items()):
        query = tdml.execute_sql(f"SHOW VIEW {old_name}").fetchall()[0][0].replace('\r','\n').lower()
        query = query.replace('create', 'replace')
        for old_sub_name, new_sub_name in mapping.items():
            query = query.replace(old_sub_name.lower(), new_sub_name.lower())
        #print(query)
        print('REPLACE VIEW ', new_name)
        tdml.execute_sql(query)

    # Construct the final view by replacing the old names with new ones in the SQL representation
    mapping[new_name] = view_name
    #query = tdml.execute_sql(f"SHOW VIEW {tddf._table_name}").fetchall()[0][0].replace('\r','\n').lower()
    #query = f'replace view {schema_name}.{view_name} AS \n' + query
    for old_name, new_name in mapping.items():
        query = query.replace(old_name.lower(), new_name.lower())

    # Execute the final query to create the main view
    #print(query)
    print('REPLACE VIEW ', view_name)
    tdml.execute_sql(query)


    # Return a teradataml DataFrame representation of the created view
    return tdml.DataFrame(tdml.in_schema(schema_name, view_name))


def crystallize_view(tddf, view_name, schema_name):

    """
    Crystallizes a given teradataml DataFrame as a view in the database with sub-views, if needed. This function
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

    return materialize_view(tddf, view_name, schema_name)