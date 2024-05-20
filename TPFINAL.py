import pandas as pd
import numpy as np
import dash
from scipy.spatial import Delaunay
from shapely.geometry import MultiPoint
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

# Load Data

spotify_top50_daily_wGenres = pd.read_csv('./data/universal_top_songs_final.csv')
enao = pd.read_csv('./data/enao.csv')

unique_countries = list(zip(spotify_top50_daily_wGenres['country'].unique(),spotify_top50_daily_wGenres['country_name'].unique()))
dropdown_options = [{'label': country_name, 'value': country_name} for country_code, country_name in unique_countries]

# Enao Alpha Shape
# Perform Delaunay triangulation
tri = Delaunay(np.column_stack((enao['left'], enao['top'])))

# Get the indices of the vertices forming the simplices
simplices = tri.simplices

# Create a polygon from the Delaunay triangulation vertices
polygon_points = []
for simplex in simplices:
    polygon_points.extend(np.array([[enao['left'][i], enao['top'][i]] for i in simplex]))
alpha_shape = MultiPoint(polygon_points).convex_hull

# Extract x and y coordinates from the alpha shape polygon
alpha_x, alpha_y = alpha_shape.exterior.xy
alpha_x = list(alpha_x)  # Convert to list
alpha_y = list(alpha_y)  # Convert to list


# Initialize Dash app
app = dash.Dash(__name__)
server = app.server
# App layout
app.layout = html.Div([
    # Page Title: Centered
    html.H1('Spotify TOP-50 Songs Visualization', style={'textAlign': 'center'}),
    html.H4('by: Arthur Silveira Franco', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Div([
            dcc.Markdown('''
                ## Musical Genre-space of Spotify Top 50 Songs
                In this section, the goal is to visualize the music genre-space of the top 50 songs in each country!
                
                ### Enao overview:
                
                
                
                To do so, I've Scrapped data from [Every Noise at Once](https://everynoise.com/),
                an ongoing attempt at an algorithmically-generated, readability-adjusted scatter-plot of the musical genre-space,
                based on data tracked and analyzed for 6,291 genre-shaped distinctions by Spotify, carried by [glenn mcdonald](https://furia.com/),
                a former Data Scientist at the company. The calibration is fuzzy, but in general down is more organic, up is more mechanical and electric;
                left is denser and more atmospheric, right is spikier and bouncier. In addition to the X and Y axies, Mcdonald used the collor-space to
                represent other analytical dimensions from the underlying music space by mapping the acoustic metrics energy, dynamic variation and instrumentalness into the 
                red, green and blue chanells respectively.
                
                On the right you can see a plot of the scrapped data, each dot represents a genre and the black line is the convex shape of Spotify's
                genre-space distribution.
                
                
                
                
            '''),
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

        html.Div([
            html.Div([
                dcc.Graph(id='ENAO-genre-space',
                    
                     figure=px.scatter(enao, x='left', y='top', height=400, width=400,
                     color='color', color_discrete_map="identity", hover_name='genre',
                     labels={
                        "top": "← organic | mechanical and electric →",
                        "left": "← denser and atmospheric | spikier and bouncier →"
                     },
                     title=f'Every Noise at Once Genre-Space')
                      .add_scatter(x=alpha_x, y=alpha_y, mode='lines', line=dict(color='black', width=0.5), showlegend=False)
                      .update_layout(xaxis=dict(range=[-100, 1550]), yaxis=dict(range=[-1000, 23500])))    
            ], style={'width':'400px','marginLeft': 'auto', 'marginRight': 'auto'})
            
        ], style={'width': '49%', 'display': 'inline-block', 'height': '400px'}),
    ], style={'display': 'flex', 'flexDirection': 'row'}),
    
    
    html.Hr(),
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

    # Replicate the Div structure and styling for the next sections
    html.Div([
        html.Div([
            dcc.Markdown('''
                ## Musical Genre-space of Spotify Top 50 Songs
                In this section, the goal is to visualize the music genre-space of the top 50 songs in each country!
                
                ### Enao overview:
                
                
                
                To do so, I've Scrapped data from [Every Noise at Once](https://everynoise.com/),
                an ongoing attempt at an algorithmically-generated, readability-adjusted scatter-plot of the musical genre-space,
                based on data tracked and analyzed for 6,291 genre-shaped distinctions by Spotify, carried by [glenn mcdonald](https://furia.com/),
                a former Data Scientist at the company. The calibration is fuzzy, but in general down is more organic, up is more mechanical and electric;
                left is denser and more atmospheric, right is spikier and bouncier. In addition to the X and Y axies, Mcdonald used the collor-space to
                represent other analytical dimensions from the underlying music space by mapping the acoustic metrics energy, dynamic variation and instrumentalness into the 
                red, green and blue chanells respectively.
                
                On the right you can see a plot of the scrapped data, each dot represents a genre and the black line is the convex shape of Spotify's
                genre-space distribution.
                
                
                
                
            '''),
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

        html.Div([
            html.Div([
                dcc.Graph(id='Enao',
                    
                     figure=px.scatter(enao, x='left', y='top', height=400, width=400,
                     color='color', color_discrete_map="identity", hover_name='genre',
                     labels={
                        "top": "← organic | mechanical and electric →",
                        "left": "← denser and atmospheric | spikier and bouncier →"
                     },
                     title=f'Every Noise at Once Genre-Space')
                      .add_scatter(x=alpha_x, y=alpha_y, mode='lines', line=dict(color='black', width=0.5), showlegend=False)
                      .update_layout(xaxis=dict(range=[-100, 1550]), yaxis=dict(range=[-1000, 23500])))    
            ], style={'width':'400px','marginLeft': 'auto', 'marginRight': 'auto'})
            
        ], style={'width': '49%', 'display': 'inline-block', 'height': '400px'}),
    ], style={'display': 'flex', 'flexDirection': 'row'}),
    
    
    html.Hr(),
    # Begining of first visualization section
    
    dcc.Markdown('''### Per Country Genre-space'''),
    html.Div([
        # Options row
        html.Div([
            html.Label(children=html.B('Choose a time span:'), style={'display': 'block'}),
            dcc.DatePickerRange(
                id='date-range-picker-rank',
                start_date=spotify_top50_daily_wGenres['snapshot_date'].min(),
                end_date=spotify_top50_daily_wGenres['snapshot_date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            html.Label(children=html.B('Choose a country:'), style={'display': 'block'}),
            dcc.Dropdown(
                id='country-dropdown-rank',
                options=dropdown_options,
                value='Global'
                # placeholder='Select a country'
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    # Interactive visualizations from the first section
    html.Div([
        dcc.Graph(id='rank-bumpchart')
        

        
    ]),
])

# Callback to update graph based on date range selection
@app.callback(
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

# Callback to update rank graph based on date range selection
@app.callback(
    Output('rank-bumpchart', 'figure'),
    [Input('date-range-picker-rank', 'start_date'),
     Input('date-range-picker-rank', 'end_date'),
     Input('country-dropdown-rank', 'value')]
)
def update_rank_bumpchart(start_date, end_date, country_name):
    
    filtered_df = filter_by_country_and_date(start_date, 
                                             end_date, 
                                             country_name)
    
    song_count = filtered_df['track_name'].value_counts().reset_index()
    song_count.columns = ['track_name', 'days_in']
    
    filtered_data_wCount = pd.merge(filtered_df, song_count, on='track_name', how='left')
    unique_songs = filtered_data_wCount.drop_duplicates(subset=['track_name'], keep='first')
    trashold = unique_songs['days_in'].sort_values(ascending=False).tolist()[30]
    most_staying_power = filtered_data_wCount[filtered_data_wCount['days_in'] >= trashold]
    
    summary_df = most_staying_power.groupby(['track_name', 'artists']).agg(mean_rank=('daily_rank', 'mean')).reset_index()
    summary_df['mean_rank'] = summary_df['mean_rank'].round(2)
    summary_df = summary_df.sort_values(by='mean_rank')
    # Sort by mean rank and get top 10
    Top10summary = summary_df.sort_values('mean_rank').head(10)

    # Join with original DataFrame
    Top10rank = pd.merge(filtered_df, Top10summary, on='track_name', how='right')
    
    fig = px.line(Top10rank, x='snapshot_date', y='daily_rank', color='track_name',
                title="Daily Ranking of the Top 10 Songs on Spotify's Global Top 50 Chart (Oct 18 - Nov 18)",
                labels={'snapshot_date': 'Date', 'daily_rank': 'Daily Rank'},
                template='plotly_dark', range_y=[50,1])
    
    
    
    # trace = go.Scatter(x=filtered_df['snapshot_date'], y=filtered_df['value'], mode='lines')
    # layout = go.Layout(title='Time Series Visualization', xaxis=dict(title='Date'), yaxis=dict(title='Value'))
    return fig


@app.callback(
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




if __name__ == '__main__':
    app.run_server(debug=True)