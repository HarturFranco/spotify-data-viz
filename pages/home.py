import dash
import pandas as pd
import numpy as np
import pickle
from scipy.spatial import Delaunay
from shapely.geometry import MultiPoint
from dash import dcc, html
import plotly.express as px

enao = pd.read_csv('./data/enao.csv')

# Enao Alpha Shape

# Load x and y coordinates from the alpha shape polygon
with open('./data/convex_hull_enao', 'rb') as file:
  alpha_x, alpha_y = pickle.load(file)

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Data and Visualizations Overview.'),
    
    dcc.Markdown('''
                 In this page you'll learn more about the goals and the data used in this visualization project, 
                 if you want to go straight to the visualization bits, and figure it out on your own, use the Menu
                 on the left to select what intrests you :)
                 '''),
    
    html.Div([
      dcc.Markdown('''
                   ## Data Domain and Sources
                   
                   
                   As you can see in the menu header, I've chosen the music domain for this project! :)
                   
                   What is music? Well, according to [Jean](https://en.wikipedia.org/wiki/Jean_Molino), music
                   is a total social fact whose definitions vary according to era and culture. Moreover,
                   the border between music and noise is aways culturally defined and there is rarely 
                   a consensus on where this border is drawn, even within a single society.
                   
                   
                   
                   Music has been described as an universal cultural element that transcends boarders and 
                   connect us as humans. Like many other media, the music consumption at this day and age 
                   is primarily stream based, and with all the complex discussions on the 
                   
                  
                   
                   
                   
                   
                   
                   
                   ''')
      
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    
    
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
                # dcc.Graph(id='ENAO-genre-space',
                    
                #      figure=px.scatter(enao, x='left', y='top', height=400, width=400,
                #      color='color', color_discrete_map="identity", hover_name='genre',
                #      labels={
                #         "top": "← organic | mechanical and electric →",
                #         "left": "← denser and atmospheric | spikier and bouncier →"
                #      },
                #      title=f'Every Noise at Once Genre-Space')
                #       .add_scatter(x=alpha_x, y=alpha_y, mode='lines', line=dict(color='black', width=0.5), showlegend=False)
                #       .update_layout(xaxis=dict(range=[-100, 1550]), yaxis=dict(range=[-1000, 23500])))    
            ], style={'width':'400px','marginLeft': 'auto', 'marginRight': 'auto'})
            
        ], style={'width': '49%', 'display': 'inline-block', 'height': '400px'}),
    ], style={'display': 'flex', 'flexDirection': 'row'}),
    
    
    html.Div('This is our Home page content.'),
])