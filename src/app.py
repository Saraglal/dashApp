#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px

df = pd.read_csv('spotify-2023.csv', encoding='latin-1' ) 


# In[2]:


df


# In[3]:


df.columns


# In[4]:


# Convert "streams" column to numeric (if it's not already numeric)
df['streams'] = pd.to_numeric(df['streams'], errors='coerce')

# Calculate the mean excluding the specified value
mean_streams = df[df.streams != df.streams.max()]['streams'].mean()

# Fill the specified value with the calculated mean
df['streams'].replace(df.streams.max(), mean_streams, inplace=True)


# In[5]:


# df['streams_M'] = pd.to_numeric(df['streams'], errors='coerce')
df['streams_M'] = df['streams'] / 1000000
df['streams_M'] = df['streams_M'].round(3)


# In[6]:


# Sort the DataFrame by the 'values' column in descending order
df_sorted = df.sort_values(by='streams', ascending=False)

# Selecting only the top 10 rows based on the 'values' column
top_10_df = df_sorted.head(10)


# In[7]:


top_10_df = top_10_df.sort_values(by='streams', ascending=False)
top_10_df


# In[8]:


# top_10_df.loc[891, 'track_name'] = 'Come Back Home'


# In[9]:


top_10_df.loc[41, 'track_name'] = 'Sunflower - Spider-Man'


# In[10]:


top_10_df.head(10)


# In[11]:


# Group by 'released_year' and 'track_name' and count the number of occurrences of each combination
count_df = df.groupby(['released_year']).size().reset_index(name='count')

# Create a line plot using Plotly Express
fig2 = px.line(count_df, x='released_year', y='count')

fig2.update_layout(title={'text': 'Growth of Songs Over the years on Spotify', 'font': {'color': '#EAF0EC'}})
fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(75,87,80,0.1)')

fig2.update_layout(
    xaxis=dict(
        tickfont=dict(color='#F6FFF9'),  # Color of x-axis labels
        title=dict(text=''),  # Color of x-axis title
    ),
    yaxis=dict(
        tickfont=dict(color='#F6FFF9'),  # Color of y-axis labels
        title=dict(text=''),  # Color of y-axis title
    ),
    margin=dict(t=50, b=0, l=0, r=0)  # Adjust layout margins to remove blank space
)

fig2.update_traces(line_color='#358455')


fig2.show()


# In[12]:


ranked_songs = top_10_df.sort_values(by="streams", ascending=False)


# In[13]:


ranked_songs


# In[14]:


fig = px.bar(ranked_songs, x='track_name', y='streams', opacity=0.5, color_discrete_sequence=['#65BA87'])

fig.update_layout(title={'text': 'Top-10 Tracks', 'font': {'color': '#F6FFF9'}})

fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(82,154,111,0.1)')

fig.update_traces(marker_line_color='black', marker_line_width=1)

fig.update_layout(
    yaxis=dict(
        tickfont=dict(color='#F6FFF9'),  # Color of x-axis labels
        title=dict(text=''),  # Color of x-axis title
        range=[-1 * ranked_songs['streams'].max() * 0.01, ranked_songs['streams'].max()]  # Expand the range to include negative values
    ),
    xaxis=dict(
        tickfont=dict(color='#F6FFF9'),  # Color of y-axis labels
        title=dict(text=''),  # Color of y-axis title
    ),
    margin=dict(t=50, b=0, l=0, r=0)  # Adjust layout margins to remove blank space
)

fig.show()


# In[15]:


# Step 1: Aggregate Streams by Artist
artist_streams = df.groupby("artist(s)_name")["streams"].sum().reset_index()

# Step 2: Rank Artists by Total Streams
ranked_artists = artist_streams.sort_values(by="streams", ascending=False)

# Step 3: Select Top 10 Artists
top_10_artists = ranked_artists.head(10)


############################################################################################

fig3 = px.bar(top_10_artists, x='artist(s)_name', y='streams', opacity=0.5, color_discrete_sequence=['#65BA87'])

fig3.update_layout(title={'text': 'Top-10 Artists', 'font': {'color': '#F6FFF9'}})

fig3.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(82,154,111,0.1)')

fig3.update_traces(marker_line_color='black', marker_line_width=1)

fig3.update_layout(
    yaxis=dict(
        tickfont=dict(color='#F6FFF9'),  # Color of x-axis labels
        title=dict(text=''),  # Color of x-axis title
        range=[-1 * top_10_artists['streams'].max() * 0.01, top_10_artists['streams'].max()]  # Expand the range to include negative values
    ),
    xaxis=dict(
        tickfont=dict(color='#F6FFF9'),  # Color of y-axis labels
        title=dict(text=''),  # Color of y-axis title
    ),
    margin=dict(t=50, b=0, l=0, r=0)  # Adjust layout margins to remove blank space
)

fig3.show()


# In[17]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State # Import Input and Output

# Load the Spotify data
similarity_df = pd.read_csv(r'similarity_df.csv', encoding='ISO-8859-1')

similarity_df.set_index('track_name', inplace=True)

app = dash.Dash(__name__)
server = app.server

placeholder_style = {
    'color': 'green',  # Placeholder text color
}

# dropdown_list_style = {
#     'backgroundColor': 'rgba(128, 128, 128, 0.5)',  # Grey color with opacity
#     'color': 'white',  # Text color
# }

# .custom-dropdown .VirtualizedSelectDropdown {
#     background-color: rgba(128, 128, 128, 0.5);  /* Grey color with opacity */
#     color: white;  /* Text color */
# }

# Define the layout with HTML and CSS
app.layout = html.Div(
    children=[
        html.Div(
            id='background',
                style={
                'position': 'relative',  # Change to relative positioning
                'width': '100%',
                'height': '100vh',  # Set height to full viewport height
                'background-image': 'url(https://wallpapers.com/images/high/plain-dark-green-wallpaper-4py2q8q4fvne42p7.webp)',  # Need to specify 'url()' for background-image
                'background-size': 'cover',  # Cover entire Div
                'background-position': 'center',  # Center the background image
            },
            children=[
                html.Div(
                    style={
                        'position': 'absolute',
                        'top': '20px',
                        'left': '0',
                        'width': '140px',
                        'height': '60px',  # Adjust height as needed for the black strip
                        'background-color': 'black',  # Black strip with 50% opacity
                    }
                ),
                html.Span('Analyze & Discover Tunes', style={'color': '#1ac877', 'position': 'absolute',
                        'font-size': '25px',
                        'top': '25px',
                        'left': '600px',
                        'width': '400px',
                        'height': '60px',
                         'font-family': 'Montserrat, sans-serif', 'font-weight': 'bold'
                        }),
                
                html.Img(
                    src='https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg',
                    style={
                        'position': 'absolute',
                        'top': '30px',  # Adjust top position to fit within black strip
                        'left': '10px',  # Adjust left position to fit within black strip
                        'height': '30px',  # Adjust height as needed
                        'width': 'auto',  # Maintain aspect ratio
                        'z-index': '1',  # Ensure logo is on top of the black strip
                    }
                ),
                dcc.Graph(id='bar-chart', figure=fig,
                style={'position': 'absolute',
                        'bottom': '30px',  # Adjust top position to fit within black strip
                        'left': '30px',  # Adjust left position to fit within black strip
                        'height': '280px',  # Adjust height as needed
                        'width': '460px',  # Maintain aspect ratio
#                         'z-index': '1', 
#                         'border': '1px solid black',
                       'border-radius': '30px',
                       'overflow': 'hidden'
                      }
                    ),
                
                dcc.Graph(id='bar-chart2', figure=fig2,
                style={'position': 'absolute',
                        'bottom': '30px',  # Adjust top position to fit within black strip
                        'left': '1030px',  # Adjust left position to fit within black strip
                        'height': '280px',  # Adjust height as needed
                        'width': '460px',  # Maintain aspect ratio
                        'z-index': '1', 
                        'border-radius': '30px',
                       'overflow': 'hidden'
                      }
                    ), 
                
                dcc.Graph(id='bar-chart3', figure=fig3,
                style={'position': 'absolute',
                        'bottom': '30px',  # Adjust top position to fit within black strip
                        'left': '530px',  # Adjust left position to fit within black strip
                        'height': '280px',  # Adjust height as needed
                        'width': '460px',  # Maintain aspect ratio
                        'z-index': '1', 
                        'border-radius': '30px',
                       'overflow': 'hidden'
                      }
                    ), 
                
                dcc.Dropdown(
                id='track-dropdown',
                options=[{'label': html.Span(track, style={'color': 'black'}), 'value': track} for track in df['track_name'].unique()],
                value='Rush',
                style={
                    'width': '50%',
                    'left': '70px',
                       'position': 'absolute',
                      'top': '15px', 
                        'backgroundColor': 'rgba(128, 128, 128, 0.5)',  # Grey color with opacity
                        'color': 'white',  # Text color
                        'placeholder': placeholder_style, 
                        'z-index':'1',
                      },
                       className='custom-dropdown',
#                        dropdownClassName='custom-dropdown-list'
                ),
                
                
                html.Div(id='track-report',
                         style={
                             'width': '70%',
                               'position': 'absolute',
                              'top': '70px',
                             'color': 'white',
                             'z-index':'0',
                         }
                         ),
                
            ]
        ),
        
        html.Div(
        className='recommender',
        style= 
            {'background-color': 'rgba(126, 189, 130, 0.5)', 
            'left': '770px',
            'height': '280px',
            'width': '250px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '-680px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
            html.Span("Similar Tracks", style={'top': '15px','font-size': '25px', 'color':'white', 'font-family': 'Palatino, Palatino Linotype, serif'}),
#             html.H1("Similar Tracks", style={''}),
            html.Div(id='output-recommendations', 
            style={
                'font-size': '20px',
                'padding-left': '-1000px',  # Add padding to indent the list items
                'margin-top': '0px',  # Add margin top to create space between title and list items
                'line-height': '2', # Adjust line height for vertical spacing
                'color':'white',
                'list-style-type': 'none'
            },
                    )]
    )
        
#                   html.Div(
#             className="card",
#             style={'background-color': 'rgba(126, 189, 130, 0.5)', 
#             'left': '30px',
#             'height': '50px',
#             'width': '200px',
#             'position': 'relative',  # Ensure absolute positioning
#             'top': '120px',
#             'padding': '20px',
#             'border-radius': '5px'
#              },
#             children=[
#                 html.Div(className="card-header", 
#                          children='Release Date', style={'font-size': '18px'}),
#                 html.Br(),  # Use <br> tag to create a new line
#                 html.Div(className="card-body", 
#                          children=f"{track_info['released_year']}/{track_info['released_month']}/{track_info['released_day']}")
#             ]
#         ),
        
            ]
        )



@app.callback(
    Output('track-report', 'children'),
     Output('output-recommendations', 'children'),
    Input('track-dropdown','value')
)

def update_report_and_recommendations(selected_track):
    # Call the update_report function to update the track report
    track_report = update_report(selected_track)
    
    # Call the get_recommendations function to get song recommendations
    recommendations = get_recommendations(selected_track)
    
    # Return both the track report and recommendations
    return track_report, recommendations

def update_report(selected_track):
    if selected_track is None:
        return html.div()

    track_info = df[df['track_name'] == selected_track].iloc[0]

    

    # Create a donut chart for danceability
    danceability_chart = px.pie(values=[track_info['danceability_%'], 100 - track_info['danceability_%']], hole=0.7, color_discrete_sequence=['#5DBC63', '#fff'], opacity=0.7)
    danceability_chart.update_traces(textinfo='none')
    danceability_chart.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    danceability_chart.add_annotation(
    text=f"{track_info['danceability_%']}%",  # You can dynamically change this text based on the percentage value
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(size=20, color='white')  # Adjust font size as needed
)
    
    # Create a donut chart for valence
    valence_chart = px.pie(values=[track_info['valence_%'], 100 - track_info['valence_%']], hole=0.7,color_discrete_sequence=['#307D35', '#fff'],opacity=0.7)
    valence_chart.update_traces(textinfo='none')
    valence_chart.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    valence_chart.add_annotation(
    text=f"{track_info['valence_%']}%",  # You can dynamically change this text based on the percentage value
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(size=20, color='white')  # Adjust font size as needed
    
)

    # Create a donut chart for energy
    energy_chart = px.pie(values=[track_info['energy_%'], 100 - track_info['energy_%']], hole=0.7, color_discrete_sequence=['#307D4F', '#fff'],opacity=0.7)
    energy_chart.update_traces(textinfo='none')
    energy_chart.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    energy_chart.add_annotation(
    text=f"{track_info['energy_%']}%",  # You can dynamically change this text based on the percentage value
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(size=20, color='white')  # Adjust font size as needed
)
    
    # Create a donut chart for energy
    acousticness_chart = px.pie(values=[track_info['acousticness_%'], 100 - track_info['acousticness_%']], hole=0.7, color_discrete_sequence=['#15C65C', '#fff'],opacity=0.7)
    acousticness_chart.update_traces(textinfo='none')
    acousticness_chart.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    acousticness_chart.add_annotation(
    text=f"{track_info['acousticness_%']}%",  # You can dynamically change this text based on the percentage value
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(size=20, color='white')  # Adjust font size as needed
)
    
    # Create a donut chart for energy
    liveness_chart = px.pie(values=[track_info['liveness_%'], 100 - track_info['liveness_%']], hole=0.7, color_discrete_sequence=['#1BEF70', '#fff'],opacity=0.7)
    liveness_chart.update_traces(textinfo='none')
    liveness_chart.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    liveness_chart.add_annotation(
    text=f"{track_info['liveness_%']}%",  # You can dynamically change this text based on the percentage value
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(size=20, color='white')  # Adjust font size as needed
)

    # Create a donut chart for energy
    speechiness_chart = px.pie(values=[track_info['speechiness_%'], 100 - track_info['speechiness_%']], hole=0.7, color_discrete_sequence=['#5FE896', '#fff'],opacity=0.7)
    speechiness_chart.update_traces(textinfo='none')
    speechiness_chart.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    speechiness_chart.add_annotation(
    text=f"{track_info['speechiness_%']}%",  # You can dynamically change this text based on the percentage value
    x=0.5,
    y=0.5,
    showarrow=False,
    font=dict(size=20, color='white')  # Adjust font size as needed
)
    
    
    track_cards = [
        html.Div(
            className="card",
            style={'background-color': 'rgba(86, 154, 91, 0.5)', 
            'left': '30px',
            'height': '50px',
            'width': '200px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '110px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
            html.Div(
                className="card-body",
                style={'font-size': '18px', 'font-family': 'Palatino, Palatino Linotype, serif'},  # Change font size
                children=[
                    "By ",  # Add space between "By" and artist name
                    html.Span(track_info['artist(s)_name'], style={'font-size': '16px'})  # Change font size for artist name
                ]
                )
                ]
                ),
        
        
        
          html.Div(
            className="card",
            style={'background-color': 'rgba(126, 189, 130, 0.5)', 
            'left': '30px',
            'height': '50px',
            'width': '200px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '120px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
                html.Div(className="card-header", 
                         children='Release Date', style={'font-size': '18px', 'font-family': 'Palatino, Palatino Linotype, serif'}),
                html.Br(),  # Use <br> tag to create a new line
                html.Div(className="card-body", 
                         children=f"{track_info['released_year']}/{track_info['released_month']}/{track_info['released_day']}")
            ]
        ),
        
        html.Div(
            className="card",
            style={'background-color': 'rgba(54, 172, 102, 0.5)', 
            'left': '30px',
            'height': '50px',
            'width': '200px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '-170px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
                html.Div(className="card-header", 
                         children='Played', style={'font-size': '18px', 'padding': '-5px','font-family': 'Palatino, Palatino Linotype, serif'}),
                html.Br(),  # Use <br> tag to create a new line
                html.Div(className="card-body", 
                         children=f"{track_info['streams_M']} M", style={'font-size': '20px'})
                
            ]
        ),

        html.Div(
            className="card",
            children=[
                html.Div(className="card-header",    
                children="Danceability\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0Valence\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0Energy",
                    
                    style={ 'background-color': 'rgba(128, 128, 128, 0.5)',
                   'padding': '10px', 
                    'position':'absolute',
                   'border-radius': '5px',
                   'left': '300px',  
                    'height': '20px',  
                    'width': '420px',
                    'top': '12px'}, 
                    ),
                
                dcc.Graph(figure=danceability_chart,
                         style={'position': 'absolute',
                        'left': '240px',  
                        'height': '250px',  
                        'width': '250px', 
                        'top': '0px'
                      }
                    ),
                        
                html.Div(className="card-header",    
                children="Acousticness\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0Liveness\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0Speechiness",
                    
                    style={ 'background-color': 'rgba(128, 128, 128, 0.5)',
                   'padding': '10px', 
                    'position':'absolute',
                   'border-radius': '5px',
                   'left': '300px',  
                    'height': '20px',  
                    'width': '420px',
                    'top': '175px'}, 
                    )
                
            ]
        ),
        html.Div(
            className="card",
            children=[
                dcc.Graph(figure=valence_chart,
                         style={'position': 'absolute',
                        'left': '390px',  
                        'height': '250px',  
                        'width': '250px',  
                        'top': '0px'
                      }
                    )
                ]
        ),
        
        html.Div(
            className="card",
            children=[
                dcc.Graph(figure=energy_chart,
                         style={'position': 'absolute',
                        'left': '535px',  
                        'height': '250px',  
                        'width': '250px', 
                        'top': '0px'
                      }
                    )
            ]
        ),
        
        html.Div(
            className="card",
            children=[
                dcc.Graph(figure=acousticness_chart,
                         style={'position': 'absolute',
                        'left': '240px',  
                        'height': '250px',  
                        'width': '250px', 
                        'top': '160px'
                      }
                    )
            ]
        ),
        
        html.Div(
            className="card",
            children=[
                dcc.Graph(figure=liveness_chart,
                         style={'position': 'absolute',
                        'left': '390px',  
                        'height': '250px',  
                        'width': '250px',  
                        'top': '160px'
                      }
                    )
                ]
        ),
                
        html.Div(
            className="card",
            children=[
                dcc.Graph(figure=speechiness_chart,
                         style={'position': 'absolute',
                        'left': '535px',  
                        'height': '250px',  
                        'width': '250px', 
                        'top': '160px'
                      }
                    )
            ]
        ), 
             html.Div(
            className="card5",
            style={'background-color': 'rgba(128, 128, 128, 0.5)', 
            'left': '1100px',
            'height': '80px',
            'width': '40px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '-40px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
            html.Div(
                className="card-body",
                style={'font-size': '18px'},  # Change font size
                children=[
                    html.Img(src="https://th.bing.com/th/id/R.994e1a5a24c7a2a3d3327fe356bd4b84?rik=Uyb3DK3jig5HCA&pid=ImgRaw&r=0", alt="Artist Image",
                             style={'height': '50px', 'width': '50px', 'margin-right': '5px'}),  # Add the image
                    html.Br(),  # Add a new line
#                     html.Br(),  # Add a new line
                    html.Span(track_info['in_apple_charts'], style={'font-size': '30px'})  # Change font size for artist name
                ]
                )
                ]
                ),
            
            html.Div(
            className="card12",
            style={'background-color': 'rgba(128, 128, 128, 0)', 
            'left': '1300px',
            'height': '80px',
            'width': '40px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '-180x',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
            html.Div(
                className="card-body",
                style={'font-size': '18px'},  # Change font size
                children=[    
                ]
                )
                ]
                ),
        
        html.Div(
            className="card7",
            style={'background-color': 'rgba(128, 128, 128, 0.5)', 
            'left': '1200px',
            'height': '80px',
            'width': '40px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '-280px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
            html.Div(
                className="card-body",
                style={'font-size': '18px'},  # Change font size
                children=[
                    html.Img(src="https://th.bing.com/th/id/R.71ba696a4a4c87fda39014c6095d1ce5?rik=mRsB2edjWjHqPA&pid=ImgRaw&r=0", alt="Artist Image", 
                             style={'height': '50px', 'width': '50px', 'margin-right': '0'}),  # Add the image
                    html.Br(),  # Add a new line
#                     html.Br(),  # Add a new line
                    html.Span(track_info['in_shazam_charts'], style={'font-size': '30px'})  # Change font size for artist name
                ]
                )
                ]
                ),
        
             html.Div(
            className="card7",
            style={'background-color': 'rgba(128, 128, 128, 0.5)', 
            'left': '1300px',
            'height': '80px',
            'width': '40px',
            'position': 'absolute',  # Ensure absolute positioning
            'top': '230px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
            html.Div(
                className="card-body",
                style={'font-size': '18px'},  # Change font size
                children=[
                    html.Img(src="https://th.bing.com/th/id/R.ad1a63272d703ea59223a7dc4be82616?rik=PvL0frac85lXCQ&riu=http%3a%2f%2fassets.stickpng.com%2fthumbs%2f6297981ce01809629f11358d.png&ehk=TippCjBmKs26CVb5%2bXHK3leW1GUuJXn9T5QR2jEE8O4%3d&risl=&pid=ImgRaw&r=0", alt="Artist Image", 
                             style={'height': '50px', 'width': '50px', 'margin-right': '0'}),  # Add the image
                    html.Br(),  # Add a new line
#                     html.Br(),  # Add a new line
                    html.Span(track_info['in_deezer_charts'], style={'font-size': '30px'})  # Change font size for artist name
                ]
                )
                ]
                ),
        
        
                html.Div(
            className="card10",
            style={'background-color': 'rgba(101, 98, 91, 0.5)', 
            'left': '1100px',
            'height': '100px',
            'width': '100px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '-632px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
            html.Div(
                className="card-body",
                style={'font-size': '18px'},  # Change font size
                children=[
                    "Added to ", 
                    html.Br(), # Add space between "By" and artist name
                    html.Span(track_info['in_spotify_playlists'], style={'font-size': '35px'}),
                    html.Br(), 
                    ' Playlists', 
                    html.Br(),
                    'on ',
                        html.Span('Spotify', style={'color': '#4ED034'})  # Make "Spotify" green

                ]
                )
                ]
                ),
        
               html.Div(
            className="card15",
            style={'background-color': 'rgba(101, 98, 91, 0.5)', 
            'left': '1280px',
            'height': '100px',
            'width': '100px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '-772px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
            html.Div(
                className="card-body",
                style={'font-size': '18px'},  # Change font size
                children=[
                    "Ranked", 
                    html.Br(), # Add space between "By" and artist name
                    html.Span(track_info['in_spotify_charts'], style={'font-size': '35px'}),
                    ' th', 
                    html.Br(),
                    
                    'on ',
                        html.Span('Spotify', style={'color': '#4ED034'})  # Make "Spotify" green

                ]
                )
                ]
                ),
        
            html.Div(
            className="card11",
            style={'background-color': 'rgba(89, 176, 12, 0.5)', 
            'left': '1100px',
            'height': '30px',
            'width': '230px',
            'position': 'relative',  # Ensure absolute positioning
            'top': '-760px',
            'padding': '20px',
            'border-radius': '5px'
             },
            children=[
            html.Div(
                className="card-body",
                style={'font-size': '20px', 'font-family': 'Palatino, Palatino Linotype, serif'},  
                children=[
                    "Explore Other Platforms"
                ]
                )
                ]
                ),
        
    ]

    return track_cards

def get_recommendations(input_song):
    recommendations = get_song_recommendations(input_song, num_recommendations=4)
    if isinstance(recommendations, list):
        list_items = [
            html.Li([
                html.Img(src='https://www.downloadclipart.net/thumb/24191-white-music-notes-vector-thumb.png', style={'width': '30px', 'height': '30px', 'margin-right': '0'}),
                song
            ], style={'border-bottom': '1px solid white'}) for song in recommendations ]
        return html.Ul(list_items, style={'list-style-type': 'none', 'padding-left': '0', 'margin-bottom': '5px'})
    else:
        return recommendations

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']


def get_song_recommendations(song_name, num_recommendations=5):
    """
    Get song recommendations based on a given song.

    Parameters:
    - song_name: Name of the song provided by the user.
    - num_recommendations: Number of songs to recommend (default is 5).

    Returns:
    - List of recommended songs.
    """
    # Check if the song is in our dataset
    if song_name not in similarity_df.index:
        return "Sorry, the song was not found in the dataset."
    
    # Get the similarity values for the given song
    song_similarities = similarity_df[song_name].sort_values(ascending=False)
    
    # Get the most similar songs (excluding the input song itself)
    recommended_songs = song_similarities.iloc[1:num_recommendations+1].index.tolist()
    
    return recommended_songs


# Run the app
if __name__ == '__main__':
    app.run_server(use_reloader=True, external_stylesheets=external_stylesheets)
    
    
    
    


# In[ ]:





# In[ ]:




