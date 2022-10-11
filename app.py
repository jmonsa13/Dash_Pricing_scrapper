# Project Pricing Mansfield

# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
from dash import Dash, html
import dash_labs as dl
import dash_bootstrap_components as dbc

from components.data_component import df, comp_df, mansfield_df
from callbacks_wholesaler import wholesaler_callbacks

# ----------------------------------------------------------------------------------------------------------------------
# Main DASH
# ----------------------------------------------------------------------------------------------------------------------
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

request_path_prefix = None

# Defining the object
app = Dash(__name__, plugins=[dl.plugins.pages], requests_pathname_prefix=request_path_prefix,
           external_stylesheets=[dbc.themes.SANDSTONE],  # MINTY, SLATE
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

# Title of the app
app.title = 'Price Monitoring | Mansfield'
# ----------------------------------------------------------------------------------------------------------------------
# Top menu, items get from all pages registered with plugin.pages
navbar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Wholesaler Price", href="/")),
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Lowe's", href='/lowes'),
                dbc.DropdownMenuItem('Others', href='/other'),
            ],
            nav=True,
            label="Consumer Price",
        ),
    ], pills=True, horizontal='end',
)
# ----------------------------------------------------------------------------------------------------------------------
# Dash layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                # Title
                dbc.Col(html.Div([html.H1(children='Price Monitoring | Mansfield',
                                          style={'textAlign': 'left'}
                                          ),
                                  html.H3(children='Kitchen & Bath',
                                          style={'textAlign': 'left'}
                                          )], id="Title",
                                 ), width=8,
                        ),
                # Tabs
                dbc.Col(html.Div(navbar,
                                 className="one-third column",
                                 id="main_tabs",
                                 style={'textAlign': 'right'}
                                 ), width=4
                        ),
            ],
            id='header', align="center", style={'height': '15%', 'margin-bottom': '20px'}
        ),

        # Line
        dbc.Row([
            html.Hr(style={'borderWidth': "5vh", "width": "100%", "borderColor": "#000000", "opacity": "unset"}),
        ],
            id='line_header', align="center", style={'margin-bottom': '20px'}
        ),

        # Content for different pages
        html.Div(
            children=dl.plugins.page_container,
            id='app-content'
        ),

    ],
    id='mainContainer',
    style={'height': '100vh'}  # "display": "flex", "flex-direction": "column"
)

# Callback
# ----------------------------------------------------------------------------------------------------------------------
# Wholesaler callback
wholesaler_callbacks(app, df, comp_df, mansfield_df)

# ----------------------------------------------------------------------------------------------------------------------
# Running the main code
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
    # app.run_server(debug=True, port=8050)
