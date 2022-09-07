# Project Pricing Mansfield
# Wholesaler price layout
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.data_component import df, comp_df, sku_list_mansfield
from components.figure_component import plot_price_index_summary

# ----------------------------------------------------------------------------------------------------------------------
# Variables definition
# ----------------------------------------------------------------------------------------------------------------------
markdown_index = '''
"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
'''

markdown_evolution = '''
"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
'''

markdown_ladder = '''
"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna 
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
'''


# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------------------------------------------------------
# Wholesaler price index layout
def wholesaler_price_index_layout():
    layout = [
        # Info message
        dcc.Markdown(children=markdown_index, style={"margin-left": "10px", "margin-top": "15px"}),

        # Division line
        dbc.Row(
            [
                html.Hr(
                    style={'borderWidth': "5vh", "width": "100%", "borderColor": "#000000", "opacity": "unset"}
                ),
            ], style={"margin-left": "5px", "margin-right": "5px"}
        ),

        # Price_index plot
        dbc.Row(
            [
                # Price_index_plot
                dbc.Col(dcc.Graph(id='Wholesaler_index_plot',
                                  figure=plot_price_index_summary(df=df, comp_df=comp_df,
                                                                  sku_list_mansfield=sku_list_mansfield,
                                                                  title=f"Mansfield Price Index", orient_h=True),
                                  hoverData={'points': [{'x': 'Alto 130 Std RF Bowl'}]},
                                  style={'width': '110%%', 'height': '50vh'}
                                  ), width='12', style={"height": "100%", "width": "100%"}
                        ),
            ], style={"margin-left": "0px", "margin-right": "0px"}
        ),

        # Title
        dbc.Row(
            [
                html.Div(
                    html.H4(id='hover_selection')
                )
            ], style={"margin-left": "5px", "margin-right": "5px", "margin-top": "15px", "margin-bottom": "10px"}
        ),

        # Information from hover
        dbc.Row(
            [
                # Image Display
                dbc.Col(
                    html.Div(
                        html.Img(id='image_hover_mansfield', alt='image',
                                 style={'height': ' 100%', 'width': '100%'}),
                    ), width=3,
                ),

                # Overall Price Index
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Overall Price Index"),
                            dbc.CardBody(
                                [
                                    html.H4(id='overall_price_index', className="card-title"),
                                ]
                            ),
                        ],
                    ), width=2,
                ),

                # Table
                dbc.Col(
                    html.Div(id='table_index_price_hover'),
                    width=6,
                ),

            ], style={"margin-left": "5px", "margin-right": "5px", "margin-bottom": "20px"}
        ),
    ]

    return layout


# Wholesaler price evolution layout
def wholesaler_price_evolution_layout():
    layout = [
        # Info message
        dcc.Markdown(children=markdown_evolution, style={"margin-left": "10px", "margin-top": "15px"}),

        # Division line
        dbc.Row(
            [
                html.Hr(
                    style={'borderWidth': "5vh", "width": "100%", "borderColor": "#000000", "opacity": "unset"}
                ),
            ], style={"margin-left": "5px", "margin-right": "5px"}
        ),

    ]

    return layout


# Wholesaler price ladder layout
def wholesaler_price_ladder_layout():
    layout = [
        # Info message
        dcc.Markdown(children=markdown_ladder, style={"margin-left": "10px", "margin-top": "15px"}),

        # Division line
        dbc.Row(
            [
                html.Hr(
                    style={'borderWidth': "5vh", "width": "100%", "borderColor": "#000000", "opacity": "unset"}
                ),
            ], style={"margin-left": "5px", "margin-right": "5px"}
        ),

    ]

    return layout
