# Project Pricing Mansfield
# Figure component
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
import numpy as np
import plotly.graph_objects as go

# ----------------------------------------------------------------------------------------------------------------------
# Variables definition
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Function Definition
# ----------------------------------------------------------------------------------------------------------------------
def plot_price_index_summary(df, comp_df, sku_list_mansfield, title, orient_h=False):
    """
    Función que crea el gráfico de historico de precio.
    :param df: data frame con los precios y la historia.
    :param title: Título de la gráfica.
    :param orient_h: Default FALSE, para poner los legend de manera horizontal.
    :return: fig: Objeto de plotly para graficar externamente.
    """
    # Initialization
    fig = go.Figure()

    # Color Scheme definition
    line_color = {'Mansfield': 'rgba(23,55,95, 1)', 'American Standard': 'rgba(0, 0, 0, 1)',
                  'Gerber': 'rgba(1, 139, 250, 1)',
                  'Western Pottery': 'rgba(148, 103, 189, 1)'}
                  # 'rgba(140, 86, 75, 1)', 'rgba(227, 119, 194, 1)', 'rgba(127, 127, 127, 1)',
                  # 'rgba(188, 189, 34, 1)', 'rgba(23, 190, 207,1)', 'rgba(31, 119, 180, 1)'}

    # Cont
    cont = 0
    flag = True

    # Products to visualize
    for i, sku_mansfield in enumerate(sku_list_mansfield):
        # sku competitors
        sku_comp = comp_df[comp_df['Homologo'] == sku_mansfield]['Sku']

        # Filter df
        df_comp = df[df['SKU_str'].isin(list(sku_comp))]

        # Calculating the price index
        df_info_price = df_comp[df_comp['Fecha'] == df_comp['Fecha'].iloc[-1]].copy()
        mansfield_ref = df_info_price[df_info_price['SKU_str'] == sku_mansfield]['Precio'].values
        mansfield_prod = df_info_price[df_info_price['SKU_str'] == sku_mansfield]['Producto'].values

        # Removing the word Mansfields
        mansfield_prod_final = [i.split('Mansfield')[-1].strip() for i in mansfield_prod]

        df_info_price['Price_index'] = np.round(((mansfield_ref / df_info_price['Precio']) * 100), 2)

        for j, product in enumerate(df_info_price['Producto_sku'].unique()):
            df_aux = df_info_price[df_info_price['Producto_sku'] == product]

            fig.add_trace(go.Scatter(x=[i], y=df_aux['Price_index'],
                                     name=df_aux['Fabricante'].iloc[0], legendgroup=df_aux['Fabricante'].iloc[0],
                                     line_color=line_color[df_aux['Fabricante'].iloc[0]],
                                     mode='markers+text', marker_symbol='diamond', marker_size=8,
                                     text=f"{df_aux['Price_index'].iloc[0]}%", textposition="middle right",
                                     showlegend=flag))
            # Changing the xlabels
            fig.data[cont].x = mansfield_prod_final
            cont += 1
        flag = False

    # Title and template
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"], title_text=title, template="seaborn")

    if orient_h is True:
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.12, xanchor="left", x=0.01),
                          legend_title="Brands")
    else:
        fig.update_layout(legend_title="Brands")

    # Update xaxis, yaxis properties
    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    fig.update_xaxes(tickangle=0, title_font = {"size": 20},)

    # Configuration
    fig.update_yaxes(title_text="% Price Index", ticksuffix="%", range=[40, 140], dtick=10)
    fig.update_traces(hovertemplate='%{y}')

    return fig
