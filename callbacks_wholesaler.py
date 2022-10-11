# Project Averias Baños y Cocina
# Callback buscar function

# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
import urllib.request
import pandas as pd
import numpy as np
from PIL import Image
from dash import Input, Output, no_update, State

from components.page_wholesaler_component import wholesaler_price_index_layout, \
    wholesaler_price_evolution_layout, wholesaler_price_ladder_layout

from components.figure_component import plot_price_index_summary, plot_price_index_evolution
from components.table_component import table_price_index_summary
from components.price_index_component import price_index_calculation


# ----------------------------------------------------------------------------------------------------------------------
# Callback
# ----------------------------------------------------------------------------------------------------------------------
# Main callback situation
def wholesaler_callbacks(app, df, comp_df, mansfield_df):
    """
    Function that contain all the callback of the app
    :param app: dash app
    :return:
    """
    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the analysis
    @app.callback(
        Output('wholesaler_price_analysis', 'children'),
        Input('wholesaler_analysis_select', 'value'))
    def analysis_selection(selection):
        if selection == 'Price Index':
            return wholesaler_price_index_layout()
        elif selection == 'Price Evolution':
            return wholesaler_price_evolution_layout()
        elif selection == 'Price Ladder':
            return wholesaler_price_ladder_layout()


    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the Linea
    @app.callback(
        Output('tipo_dropdown', 'options'),
        Input('subcategory_dropdown', 'value'))
    def tipo_unico(subcategory):
        # Filter by subcategory
        df_aux_subcategory = mansfield_df[mansfield_df['Subcategory'] == subcategory]

        return df_aux_subcategory['Tipo'].dropna().unique()


    # ------------------------------------------------------------------------------------------------------------------
    # Callback for changing the Linea
    @app.callback(
        Output('product_dropdown', 'options'),
        Output('product_dropdown', 'value'),
        Input('subcategory_dropdown', 'value'),
        Input('tipo_dropdown', 'value'))
    def product_unico(subcategory, tipo):
        if subcategory != 'Lavs' and tipo is not None:
            # Filter by subcategory
            df_aux = mansfield_df[mansfield_df['Subcategory'] == subcategory]

            # Filter by type
            df_aux_tipo = df_aux[df_aux['Tipo'] == tipo]

            # Unique list
            product_lista = df_aux_tipo['Description'].dropna().unique()

            return product_lista, []

        elif subcategory == 'Lavs':
            # Filter by subcategory
            df_aux = mansfield_df[mansfield_df['Subcategory'] == subcategory]

            # Unique list
            product_lista = df_aux['Description'].dropna().unique()

            return product_lista, []

        else:
            return [], []

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for searching the info
    @app.callback(
        Output('Wholesaler_index_plot', 'figure'),
        Output('Wholesaler_index_plot', 'hoverData'),
        Output('Wholesaler_index_plot', 'style'),
        Input('product_dropdown', 'value'),
        Input('product_dropdown', 'options'))
    def wholesaler_price_index_plot(products, update_options_products):
        # Enter if product was selected
        if products is not None and len(products) != 0 and len(update_options_products) != 0:
            # Filter df mansfield
            sku_list_mansfield = mansfield_df[mansfield_df['Description'].isin(list(products))]['Sku']

            figure = plot_price_index_summary(df=df, comp_df=comp_df,
                                              sku_list_mansfield=sku_list_mansfield,
                                              title=f"Mansfield Price Index", orient_h=False)

            hoverData = {'points': [{'x': products[0]}]}

            return figure, hoverData, dict(display='block')
        else:
            return no_update, no_update, dict(display='none')

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for searching the info
    @app.callback(
        Output('Wholesaler_index_plot_evolution', 'figure'),
        Output('Wholesaler_index_plot_evolution', 'hoverData'),
        Output('Wholesaler_index_plot_evolution', 'style'),
        Input('Wholesaler_index_plot', 'hoverData'),
        State('product_dropdown', 'value'))
    def wholesaler_price_index_evolution_plot(hoverData, products_list):
        # Enter if product was selected
        if products_list is not None and len(products_list) != 0:
            # Mansfield product to compare
            mansfield_product_sel = hoverData['points'][0]['x']

            # Filter df mansfield
            sku_mansfield = mansfield_df[mansfield_df['Description'] == mansfield_product_sel]['Sku']

            figure, hoverData = plot_price_index_evolution(df=df, comp_df=comp_df,
                                                sku_mansfield=sku_mansfield,
                                                title=f"Mansfield {mansfield_product_sel} Price Index Evolution",
                                                orient_h=True)

            return figure, hoverData, dict(display='block')
        else:
            return no_update, hoverData, dict(display='none')

    # ------------------------------------------------------------------------------------------------------------------
    # Callback for searching the info
    @app.callback(
        Output('table_index_price_hover', 'children'),
        Output('overall_price_index', 'children'),
        Output('figure_name_selection_evolution', 'children'),
        Output('image_hover_mansfield', 'src'),
        Output('price_index_detail', 'style'),
        Input('Wholesaler_index_plot', 'hoverData'),
        Input('Wholesaler_index_plot_evolution', 'hoverData'),
        Input('product_dropdown', 'value'))
    def wholesaler_table_index(hoverData, hoverData_evolution, products_list):
        if products_list is not None and len(products_list) != 0:
            # ----------------------------------------------------------------------------------------------------------
            # Hover info from price index
            # ----------------------------------------------------------------------------------------------------------
            # Mansfield product to compare
            mansfield_product_sel = hoverData['points'][0]['x']

            # ----------------------------------------------------------------------------------------------------------
            # Hover info from evolution price index
            # ----------------------------------------------------------------------------------------------------------
            # Product and date to display
            date_sel = hoverData_evolution['points'][0]['x']
            product_sel = hoverData_evolution['points'][0]['customdata']
            message_hover = f'{product_sel}'

            # ----------------------------------------------------------------------------------------------------------
            # Mansfield filtering
            # ----------------------------------------------------------------------------------------------------------
            # Filtering by the mansfield product
            df_mansfield = df[df['Producto'] == mansfield_product_sel].copy()
            sku_mansfield = df_mansfield.iloc[-1]['SKU']

            # ----------------------------------------------------------------------------------------------------------
            # Competitor filtering
            # ----------------------------------------------------------------------------------------------------------
            # sku competitors
            sku_comp = comp_df[comp_df['Homologo'] == sku_mansfield]['Sku']

            # Filter df competitor
            df_comp = df[df['SKU_str'].isin(list(sku_comp))].copy()

            # ----------------------------------------------------------------------------------------------------------
            # Price Index
            # ----------------------------------------------------------------------------------------------------------
            # Price index into dataframe
            df_comp['Price_index'] = price_index_calculation(df_comp, df_mansfield)
            df_mansfield['Price_index'] = 100.0

            # ----------------------------------------------------------------------------------------------------------
            # Global dataframe competitors + mansfield
            # ----------------------------------------------------------------------------------------------------------
            # Concat the two dataframe
            df_info_price = pd.concat([df_comp, df_mansfield])
            df_price_index = df_info_price[df_info_price['Fecha'] == date_sel].copy()

            # ----------------------------------------------------------------------------------------------------------
            # Image requesting
            # ----------------------------------------------------------------------------------------------------------
            # Requesting the image
            url_product = df_price_index[df_price_index['Producto'] == product_sel]["Image_url"].iloc[0]
            url_product = url_product.replace(" ", "%20")
            urllib.request.urlretrieve(url_product, "./images/image_mansfield.png")
            image = Image.open('./images/image_mansfield.png')

            # ----------------------------------------------------------------------------------------------------------
            # Overall price index
            # ----------------------------------------------------------------------------------------------------------
            # Calculating overall price index
            overall_price_index = np.round((df_price_index['Price_index'].abs().sum() - 100) /
                                           (len(df_price_index) - 1), 2)

            # Dash Table
            # Convertion for dash table
            df_table = df_price_index[['Fecha', 'Fabricante', 'Producto', 'Market_Place',
                                       'Precio_wholesaler', 'Price_index', 'URL']]

            # Renaming to English
            df_table.columns = ['Date', 'Brand', 'Product', 'Market Place',
                                'Price Wholesaler (usd)', 'Price Index (%)', 'Url']

            # Table
            table = table_price_index_summary(df_table)

            return table, str(overall_price_index) + '%', message_hover, image, dict(display='block')
        else:
            return no_update, no_update, no_update, no_update, dict(display='none')


