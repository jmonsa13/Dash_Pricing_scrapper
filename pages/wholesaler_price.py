# Project Pricing Mansfield
# Wholesaler price layout
# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page

from components.wholesaler_component import wholesaler_price_index_layout, \
    wholesaler_price_evolution_layout, wholesaler_price_ladder_layout


# dash-labs plugin call, menu name and route
register_page(__name__, path='/')
# ----------------------------------------------------------------------------------------------------------------------
# Variables definition
# ----------------------------------------------------------------------------------------------------------------------
markdown_text = '''
On this page, the wholesaler price will be analyzed for different marketplaces.
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
            dcc.Markdown(children=markdown_text),

            # Price Index
            html.H3(children='1) Price Index', style={"margin-left": "10px", 'margin-top': '40px'}),
            html.Div(children=wholesaler_price_index_layout(),
                     id='wholesaler_price_index'
                     ),

            # Price Evolution
            html.H3(children='2) Price Evolution', style={"margin-left": "10px", 'margin-top': '40px'}),
            html.Div(children=wholesaler_price_evolution_layout(),
                     id='wholesaler_price_evolution'
                     ),

            # Price Ladder
            html.H3(children='2) Price Ladder', style={"margin-left": "10px", 'margin-top': '40px'}),
            html.Div(children=wholesaler_price_ladder_layout(),
                     id='wholesaler_price_ladder'
                     ),
        ],
    )
)
