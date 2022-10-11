# Project Pricing Mansfield
# Figure component
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go
from components.price_index_component import price_index_calculation
# ----------------------------------------------------------------------------------------------------------------------
# Variables definition
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Function Definition
# ----------------------------------------------------------------------------------------------------------------------
def plot_price_index_summary(df, comp_df, sku_list_mansfield, title, orient_h=False):
    """
    Función que crea el gráfico de price index.
        :param df: data frame con los precios y la historia.
        :param comp_df: Competitor master base dataframe
        :param sku_list_mansfield: List with the sku from mansfield used to compare with competitors and plot.
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
        # --------------------------------------------------------------------------------------------------------------
        # Competitor filtering
        # --------------------------------------------------------------------------------------------------------------
        # sku competitors
        sku_comp = comp_df[comp_df['Homologo'] == sku_mansfield]['Sku']

        # Filter df competitor
        df_comp = df[df['SKU_str'].isin(list(sku_comp))].copy()

        # --------------------------------------------------------------------------------------------------------------
        # Mansfield filtering
        # --------------------------------------------------------------------------------------------------------------
        # Filtering by the mansfield product
        df_mansfield = df[df['SKU_str'] == sku_mansfield].copy()

        # --------------------------------------------------------------------------------------------------------------
        # Price Index
        # --------------------------------------------------------------------------------------------------------------
        # Price index into dataframe
        df_comp['Price_index'] = price_index_calculation(df_comp, df_mansfield)
        df_mansfield['Price_index'] = 100.0

        # --------------------------------------------------------------------------------------------------------------
        # Global dataframe competitors + mansfield
        # --------------------------------------------------------------------------------------------------------------
        # Concat the two dataframe
        df_info_price = pd.concat([df_comp, df_mansfield])
        df_price_index = df_info_price[df_info_price['Fecha'] == df_info_price['Fecha'].iloc[-1]].copy()

        # Mansfield name recovering
        mansfield_prod = df_price_index[df_price_index['SKU_str'] == sku_mansfield]['Producto'].values

        for j, product in enumerate(df_price_index['Producto_sku'].unique()):
            df_aux = df_price_index[df_price_index['Producto_sku'] == product]

            fig.add_trace(go.Scatter(x=[i], y=df_aux['Price_index'],
                                     name=df_aux['Fabricante'].iloc[0], legendgroup=df_aux['Fabricante'].iloc[0],
                                     line_color=line_color[df_aux['Fabricante'].iloc[0]],
                                     mode='markers+text', marker_symbol='diamond', marker_size=8,
                                     text=f"{df_aux['Price_index'].iloc[0]}%", textposition="middle right",
                                     showlegend=flag,
                                     hovertemplate=df_aux['Producto'].iloc[0]
                                     )
                          )
            # Changing the xlabels
            fig.data[cont].x = mansfield_prod
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
    fig.update_xaxes(tickangle=0, title_font={"size": 20})

    # Configuration
    fig.update_yaxes(title_text="% Price Index", ticksuffix="%", dtick=10)
    #fig.update_traces(hovertemplate='%{y}')

    return fig

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def plot_price_index_evolution(df, comp_df, sku_mansfield, title, orient_h=False):
    """
    Función que crea el gráfico de historico de price index.
        :param df: data frame con los precios y la historia.
        :param comp_df: Competitor master base dataframe
        :param sku_mansfield: Sku from mansfield used to compare with competitors and plot.
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

    # --------------------------------------------------------------------------------------------------------------
    # Competitor filtering
    # --------------------------------------------------------------------------------------------------------------
    # sku competitors
    sku_comp = comp_df[comp_df['Homologo'] == sku_mansfield.iloc[0]]['Sku']

    # Filter df competitor
    df_comp = df[df['SKU_str'].isin(list(sku_comp))].copy()

    # --------------------------------------------------------------------------------------------------------------
    # Mansfield filtering
    # --------------------------------------------------------------------------------------------------------------
    # Filtering by the mansfield product
    df_mansfield = df[df['SKU_str'] == sku_mansfield.iloc[0]].copy()

    # --------------------------------------------------------------------------------------------------------------
    # Price Index
    # --------------------------------------------------------------------------------------------------------------
    # Price index into dataframe
    df_comp['Price_index'] = price_index_calculation(df_comp, df_mansfield)
    df_mansfield['Price_index'] = 100.0

    # --------------------------------------------------------------------------------------------------------------
    # Global dataframe competitors + mansfield
    # --------------------------------------------------------------------------------------------------------------
    # Concat the two dataframe
    df_price_index = pd.concat([df_comp, df_mansfield])

    for j, product in enumerate(df_price_index['Producto_sku'].unique()):
        df_aux = df_price_index[df_price_index['Producto_sku'] == product]

        fig.add_trace(go.Scatter(x=df_aux['Fecha'], y=df_aux['Price_index'],
                                 name=df_aux['Producto'].iloc[0],
                                 line_color=line_color[df_aux['Fabricante'].iloc[0]],
                                 mode='lines+markers', marker_size=4,
                                 customdata=df_aux['Producto']
                                 #hovertemplate='%{y}'
                                 )
                      )

    hoverData = {'points': [{'x': df_aux['Fecha'].iloc[-1], 'customdata': df_aux['Producto'].iloc[0]}]}

    # Title and template
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"], title_text=title, template="seaborn")

    if orient_h is True:
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=1.12, xanchor="left", x=0.15),
                          legend_title="Products")
    else:
        fig.update_layout(legend_title="Products")

    # Update xaxis, yaxis properties
    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    # Configuration
    fig.update_yaxes(title_text="% Price Index", ticksuffix="%", dtick=10)
    fig.update_xaxes(title_text="Date")

    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
            ])
        )
    )

    return fig, hoverData
