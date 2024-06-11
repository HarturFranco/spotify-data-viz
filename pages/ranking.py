import pandas as pd
import numpy as np
import itertools
import dash
from dash import dcc, html, callback, Input, Output
# from dash.dependencies import Input, Output
import plotly.express as px

# Load Data

spotify_top50_daily_wGenres = pd.read_csv('./data/universal_top_songs_final.csv')

unique_countries = list(zip(spotify_top50_daily_wGenres['country'].unique(),spotify_top50_daily_wGenres['country_name'].unique()))
dropdown_options = [{'label': country_name, 'value': country_name} for country_code, country_name in unique_countries]

# Initialize Dash page
dash.register_page(__name__)

# page layout
layout = html.Div([

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


# Callback to update rank graph based on date range selection
@callback(
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
    
    # # Adding rank gaps
    # dr = pd.date_range(start_date, end_date, freq='d')
    
    # # Creating dummy data for consistent gaps:

    # # Step 1: Get unique music_id and snapshot_date values
    # unique_spotify_ids = Top10rank['spotify_id'].unique()

    # # Step 2: Create all combinations of music_id and snapshot_date
    # all_combinations = list(itertools.product(unique_spotify_ids, dr))

    # # Step 3: Convert the combinations into a DataFrame
    # df_all_combinations = pd.DataFrame(all_combinations, columns=['spotify_id', 'snapshot_date'])
    # df_all_combinations['snapshot_date'] = df_all_combinations['snapshot_date'].astype(str)

    # # Step 4: Merge with the original DataFrame to fill missing rows
    # Top10rank_with_gap_data = pd.merge(df_all_combinations, Top10rank, on=['spotify_id', 'snapshot_date'], how='left')
    
    # Top10rank_with_gap_data.to_csv('bd.csv')
    Top10rank_sorted = Top10rank.sort_values(by='snapshot_date')
    fig = px.scatter(Top10rank_sorted, x='snapshot_date', y='daily_rank', color='track_name',
                title=f"Daily Ranking of the Top 10 Songs on Spotify's {country_name} Top 50 Chart",
                labels={'snapshot_date': 'Date', 'daily_rank': 'Daily Rank'},#template='plotly_dark',
                range_y=[50,1])
    fig.update_traces(mode='lines')
    fig.update_layout(legend=dict(
        orientation="h",
        # entrywidth=70,
        yanchor="bottom",
        y=-0.50,
        xanchor="right",
        x=1
    ))
    
    # trace = go.Scatter(x=filtered_df['snapshot_date'], y=filtered_df['value'], mode='lines')
    # layout = go.Layout(title='Time Series Visualization', xaxis=dict(title='Date'), yaxis=dict(title='Value'))
    return fig


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

