import pandas as pd
import numpy as np
import dash
import pickle
from scipy.spatial import Delaunay
from shapely.geometry import MultiPoint
from dash import dcc, html, dash_table, callback, Input, Output
# from dash.dependencies import 
import plotly.express as px

# Load Data

spotify_top50_daily_wGenres = pd.read_csv('./data/universal_top_songs_final.csv')
enao = pd.read_csv('./data/enao.csv')

unique_countries = list(zip(spotify_top50_daily_wGenres['country'].unique(),spotify_top50_daily_wGenres['country_name'].unique()))
dropdown_options = [{'label': country_name, 'value': country_name} for country_code, country_name in unique_countries]

# Enao Alpha Shape

# Load x and y coordinates from the alpha shape polygon
with open('./data/convex_hull_enao', 'rb') as file:
  alpha_x, alpha_y = pickle.load(file)



# Initialize Dash page
dash.register_page(__name__)


# App layout
layout = html.Div([
   
    
    
    
    
    # Begining of first visualization section
    
    dcc.Markdown('''### Per Country Genre-space'''),
    html.Div([
        # Options row
        html.Div([
            html.Label(children=html.B('Choose a time span:'), style={'display': 'block'}),
            dcc.DatePickerRange(
                id='date-range-picker',
                start_date=spotify_top50_daily_wGenres['snapshot_date'].min(),
                end_date=spotify_top50_daily_wGenres['snapshot_date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            html.Label(children=html.B('Choose a country:'), style={'display': 'block'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=dropdown_options,
                value='Global'
                # placeholder='Select a country'
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    # Interactive visualizations from the first section
    html.Div([
        html.Div([
            dcc.Graph(id='enao-graph')
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

        html.Div([
            html.H2(id='table-title'),
            dash_table.DataTable(
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': '10px',
                },
                id='music-table',
                columns=[{'name': 'Music', 'id': 'track_name'}, {'name': 'Artists', 'id': 'artists'}],
                data=[],
                page_size=20
            )
        ], style={'width': '49%', 'display': 'inline-block', 'height': '800px'}),
    ], style={'display': 'flex', 'flexDirection': 'row'}),

    
])

# Callback to update graph based on date range selection
@callback(
    Output('enao-graph', 'figure'),
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date'),
     Input('country-dropdown', 'value')]
)
def update_graph(start_date, end_date, country_name):
    
    filtered_df = filter_by_country_and_date(start_date, 
                                             end_date, 
                                             country_name, 
                                             drop_duplicates=True, 
                                             drop_subset='spotify_id', 
                                             cols=['spotify_id', 'track_name', 'artists', 'daily_rank', 'daily_movement', 'popularity', 'is_explicit', 'genres'])
    
    # Split genres in df_songs into individual rows
    filtered_data_gere_exp = filtered_df.assign(genres=filtered_df['genres'].str.split(', ')).explode('genres')
    genre_counts = filtered_data_gere_exp['genres'].value_counts().reset_index()
    genre_counts.columns = ['genre', 'song_count']

    plot_data_enao = pd.merge(enao, genre_counts, on='genre', how='inner')
    
    
    # Create the scatter plot with alpha shape line
    fig = px.scatter(plot_data_enao, x='left', y='top',height=800, size='song_count',
                     color='color', color_discrete_map="identity", hover_name='genre',
                     labels={
                        "top": "← organic | mechanical and electric →",
                        "left": "← denser and atmospheric | spikier and bouncier →"
                     },
                     title=f'Genres in {country_name}')
    fig.update_traces(marker=dict(opacity=0.8))
    fig.add_scatter(x=alpha_x, y=alpha_y, mode='lines', line=dict(color='black', width=0.5), showlegend=False)
    fig.update_layout(xaxis=dict(range=[-100, 1550]), yaxis=dict(range=[-1000, 23500]))
    
    
    
    # trace = go.Scatter(x=filtered_df['snapshot_date'], y=filtered_df['value'], mode='lines')
    # layout = go.Layout(title='Time Series Visualization', xaxis=dict(title='Date'), yaxis=dict(title='Value'))
    return fig


@callback(
    [Output('table-title', 'children'),
     Output('music-table', 'data')],
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date'),
     Input('country-dropdown', 'value'),
     Input('enao-graph', 'clickData')]
)
def update_table(start_date, end_date, country_name, clickData):
    
    filtered_df = filter_by_country_and_date(start_date, 
                                             end_date, 
                                             country_name, 
                                             drop_duplicates=True, 
                                             drop_subset='spotify_id', 
                                             cols=['spotify_id', 'track_name', 'artists', 'genres'])
    
    # Split genres in df_songs into individual rows
    filtered_data_gere_exp = filtered_df.assign(genres=filtered_df['genres'].str.split(', ')).explode('genres')

    title = " Songs in " + country_name
    if clickData:
        genre = clickData['points'][0]['hovertext']
        data_table = filtered_data_gere_exp[(filtered_data_gere_exp['genres'] == genre)]
        data_table = data_table[['track_name', 'artists']]
        title = genre + title
    else:
        data_table = filtered_df[['track_name', 'artists']]

    
    return title, data_table.to_dict('records')


# Auxiliar Functions

def filter_by_country_and_date(start_date, end_date, country_name, drop_duplicates=False, drop_subset=None, cols=[]):
    
    date_country_filtered = spotify_top50_daily_wGenres[(spotify_top50_daily_wGenres['snapshot_date'] >= start_date) &
                                              (spotify_top50_daily_wGenres['snapshot_date'] <= end_date) & 
                                              (spotify_top50_daily_wGenres['country_name'] == country_name)
                                              ]
    
    if drop_duplicates:
        date_country_filtered = date_country_filtered.drop_duplicates(subset=drop_subset, keep='first')
    
    if cols:
        date_country_filtered = date_country_filtered[cols]
    
    return date_country_filtered
