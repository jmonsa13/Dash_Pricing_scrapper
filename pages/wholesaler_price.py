# Project Pricing Mansfield
# Wholesaler price layout
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page

# dash-labs plugin call, menu name and route
register_page(__name__, path='/')
# ----------------------------------------------------------------------------------------------------------------------
# Variables definition
# ----------------------------------------------------------------------------------------------------------------------
markdown_text = '''
On this page, the wholesaler price will be analyzed for different marketplaces. Please choose a type of analysis 
between price index analysis, price evolution analysis, and price ladder.
'''

# ----------------------------------------------------------------------------------------------------------------------
# Layout for Wholesaler Page
# ----------------------------------------------------------------------------------------------------------------------
layout = dbc.Container(
    html.Div(
        [
            # Title of the pages
            html.H2(children='Wholesaler Price', style={"margin-left": "5px", 'margin-bottom': '20px'}),

            # Content markdown
            dcc.Markdown(children=markdown_text, style={"margin-left": "5px"}),

            # Type of analysis
            dbc.Row(
                [
                    dbc.Col(
                        html.H4(children='Select type of analysis:'), width=3,
                    ),
                    dbc.Col(
                        dcc.RadioItems(
                            options=['Price Index', 'Price Evolution', 'Price Ladder'],
                            value='Price Index',
                            inline=True,
                            labelStyle={"margin-right": "30px"},
                            id='wholesaler_analysis_select',
                        ), width=6,
                    ),
                ], style={"margin-left": "0px", 'margin-top': '20px', 'margin-bottom': '10px'}

            ),

            # Price Analysis
            html.Div(id='wholesaler_price_analysis')
        ],
    )
)
