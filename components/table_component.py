# Project Pricing Mansfield
# Table component
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
from dash import dash_table

# ----------------------------------------------------------------------------------------------------------------------
# Variables definition
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Function Definition
# ----------------------------------------------------------------------------------------------------------------------
def table_price_index_summary(df):
    """
    Función que muestra una tabla usando dash.
        :param df: pandas dataframe
        :return: dash table
    """
    data = df.to_dict('records')
    columns = [{"name": i.capitalize(), "id": i, } for i in (df.columns)]

    table = dash_table.DataTable(data=data, columns=columns,
                                 page_size=10,
                                 editable=False,  # allow editing of data inside all cells
                                 filter_action="none",  # allow filtering of data by user ('native') or not ('none')
                                 sort_action="native",  # enables data to be sorted per-column by user or not ('none')
                                 sort_mode="multi",  # sort across 'multi' or 'single' columns
                                 style_data={
                                     'whiteSpace': 'normal',
                                     'height': 'auto',
                                     'lineHeight': '15px'
                                 },
                                 css=[{
                                     'selector': '.dash-spreadsheet td div',
                                     'rule': '''
                                               line-height: 15px;
                                               max-height: 30px; min-height: 30px; height: 30px;
                                               display: block;
                                               overflow-y: hidden;
                                               '''
                                 }],
                                 tooltip_data=[
                                     {
                                         column: {'value': str(value), 'type': 'markdown'}
                                         for column, value in row.items()
                                     } for row in df.to_dict('records')
                                 ],
                                 tooltip_duration=None,
                                 style_cell={
                                     'textAlign': 'center',
                                     'minWidth': '120px', 'width': '120px', 'maxWidth': '200px',
                                     'fontSize': 12, 'font-family': 'sans-serif',
                                     'height': 'auto', 'whiteSpace': 'normal'
                                 },  # left align text in columns for readability
                                 style_table={'overflowX': 'auto'},
                                 style_header={
                                     'fontWeight': 'bold',
                                     'backgroundColor': 'rgb(210, 210, 210)',
                                 },
                                 style_data_conditional=[
                                     {
                                         'if': {'row_index': 'odd'},
                                         'backgroundColor': 'rgb(250, 250, 250)',
                                     }
                                 ],
                                 )
    return table
