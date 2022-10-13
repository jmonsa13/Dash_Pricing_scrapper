# Project Pricing Mansfield
# Wholesaler price layout
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.data_component import mansfield_df

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
        # Title
        html.H3(children='1) Price Index', style={"margin-left": "10px", 'margin-top': '40px'}),

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
        # --------------------------------------------------------------------------------------------------------------
        # Filtering
        # --------------------------------------------------------------------------------------------------------------
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H6("Subcategory",
                                style={'font-weight': 'bold', 'margin-bottom': "10px"}),
                        dcc.Dropdown(options=mansfield_df['Subcategory'].dropna().unique(),
                                     id='subcategory_dropdown'),
                    ], width=2
                ),
                dbc.Col(
                    [
                        html.H6("Type",
                                style={'font-weight': 'bold', 'margin-bottom': "10px"}),
                        dcc.Dropdown(id='tipo_dropdown'),
                    ], width=2
                ),
                dbc.Col(
                    [
                        html.H6("Products",
                                style={'font-weight': 'bold', 'margin-bottom': "10px"}),
                        dcc.Dropdown(id='product_dropdown', multi=True),
                    ], width=8
                ),
                # dbc.Col(
                #     [
                #         html.Div(dbc.Button("Analysis", id="Analizar_wholesaler", className="me-1", n_clicks=0,
                #                             color="primary"),
                #                  className="d-grid gap-2 col-4 mx-auto"),
                #     ], width=2,  id='buttons', align="center"
                # ),
            ], style={"margin-left": "5px", "margin-right": "5px"}
        ),
        # --------------------------------------------------------------------------------------------------------------
        # Price_index plot
        # --------------------------------------------------------------------------------------------------------------
        dbc.Row(
            [
                # Price_index_plot
                dbc.Col(dcc.Graph(id='Wholesaler_index_plot',
                                  style={'width': '110%%', 'height': '50vh', 'display': 'none'}
                                  ), width='12', style={"height": "100%", "width": "100%"}
                        ),
            ], style={"margin-left": "0px", "margin-right": "0px"}
        ),

        # --------------------------------------------------------------------------------------------------------------
        # Price index detail
        # --------------------------------------------------------------------------------------------------------------
        html.Div(
            [
                # Title
                dbc.Row(
                    [
                        html.Div(
                            html.H4(children='Price Index Evolution', id='hover_selection_detail')
                        ),
                    ]
                ),

                # Price Index Evolution
                dbc.Row(
                    [
                        # Price_index_plot
                        dbc.Col(
                            dcc.Graph(
                                id='Wholesaler_index_plot_evolution',
                                style={'width': '110%%', 'height': '50vh', 'display': 'none'}
                            ), width=10,
                        ),
                        # Image Display
                        dbc.Col(
                            [
                                html.Div(
                                    html.H5(children='Product Image')
                                ),
                                html.Div(
                                    html.Img(id='image_hover_mansfield', alt='image',
                                             style={'height': ' 100%', 'width': '100%'}),
                                ),
                                html.Div(
                                    html.P(id='figure_name_selection_evolution',
                                           style={'font-size': '14px'})
                                ),
                            ], width=2,
                        ),
                    ],
                    style={"margin-left": "5px", "margin-right": "5px", "margin-bottom": "10px"},
                    align="center",
                ),

                # Title detail of hover data price index evolution
                dbc.Row(
                    [
                        html.Div(
                            html.H6(children='Detail Price Index Evolution')
                        ),
                    ]
                ),

                # Information from hover
                dbc.Row(
                    [
                        # Table
                        dbc.Col(
                            html.Div(id='table_index_price_hover'),
                            width=10,
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
                    ], style={"margin-left": "5px", "margin-right": "5px", "margin-bottom": "20px"},
                ),
            ], style={"margin-left": "5px", "margin-right": "5px", "margin-bottom": "20px", 'display': 'none'},
            id='price_index_detail'
        ),
    ]

    return layout


# Wholesaler price evolution layout
def wholesaler_price_evolution_layout():
    layout = [
        # Title
        html.H3(children='2) Price Evolution', style={"margin-left": "10px", 'margin-top': '40px'}),

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
        # Title
        html.H3(children='3) Price Ladder', style={"margin-left": "10px", 'margin-top': '40px'}),

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
