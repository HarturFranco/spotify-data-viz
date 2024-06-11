import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pickle

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}



app.layout = html.Div([
  
   html.Div(
    [
        html.H1("Spotify TOP-50 Songs Visualization", className="display-8"),
        # html.P(
        #     "by: Arthur Silveira Franco", className="lead"
        # ),
        html.Hr(),
        dbc.Nav(
            [
              html.Div(
                dbc.NavLink(f"{page['name']} - {page['path']}", href=page["relative_path"], active="exact")
              ) for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
  ),
  html.Div([dash.page_container], style=CONTENT_STYLE),
])

if __name__ == '__main__':
    # app.run(debug=True)
    app.run_server(debug=True)