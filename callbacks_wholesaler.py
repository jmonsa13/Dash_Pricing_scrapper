# Project Averias Baños y Cocina
# Callback buscar function

# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
import urllib.request
import numpy as np
from PIL import Image
from dash import Input, Output, dash_table


# ----------------------------------------------------------------------------------------------------------------------
# Callback
# ----------------------------------------------------------------------------------------------------------------------
# Main callback situation
def wholesaler_callbacks(app, df, comp_df, Mansfield_df):
    """
    Function that contain all the callback of the app
    :param app: dash app
    :param df_maquinas: panda dataframe containing the división, planta & linea
    :return:
    """
    # ------------------------------------------------------------------------------------------------------------------
    # Callback for searching the info
    @app.callback(
        Output('table_index_price_hover', 'children'),
        Output('overall_price_index', 'children'),
        Output('hover_selection', 'children'),
        Output('image_hover_mansfield', 'src'),
        Input('Wholesaler_index_plot', 'hoverData'))
    def wholesaler_table_index(hoverData):
        # Mansfield product to compare
        mansfield_product_sel = 'Mansfield ' + hoverData['points'][0]['x']
        message_hover = f'Information of {mansfield_product_sel}'

        mansfield_product = Mansfield_df[Mansfield_df['Producto'] == mansfield_product_sel]
        sku_mansfield = mansfield_product.iloc[-1]['SKU']

        # Requesting the image
        urllib.request.urlretrieve(mansfield_product["Image_url"].iloc[-1], "./images/image_mansfield.png")
        image = Image.open('./images/image_mansfield.png')

        # Products to visualize
        sku_comp = comp_df[comp_df['Homologo'] == str(sku_mansfield)]['Sku']

        # Filter df
        df_comp = df[df['SKU_str'].isin(list(sku_comp))]

        # Price index
        df_info_price = df_comp[df_comp['Fecha'] == df_comp['Fecha'].iloc[-1]].copy()
        mansfield_ref = df_info_price[df_info_price['Producto'] == mansfield_product_sel]['Precio'].values
        df_info_price['Price_index'] = np.round(((mansfield_ref / df_info_price['Precio']) * 100), 2)

        # Calculating overall price index
        overall_price_index = np.round((df_info_price['Price_index'].abs().sum() - 100) / (len(df_info_price) - 1), 2)

        # Dash Table
        # Convertion for dash table
        df_table = df_info_price[['Fabricante', 'Producto', 'Market_Place', 'Precio', 'Price_index', 'URL']]

        # Renaming to English
        df_table.columns = ['Brand', 'Product', 'Market Place', 'Price (usd)', 'Price Index (%)', 'Url']
        data = df_table.to_dict('records')
        columns = [{"name": i.capitalize(), "id": i, } for i in (df_table.columns)]

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
                                         } for row in df_table.to_dict('records')
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

        return table, str(overall_price_index) + '%', message_hover, image

