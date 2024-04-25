import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load the Spotify data
similarity_df = pd.read_csv(r'D:\ITI\23.Data Visualization\Dash Project\similarity_df.csv', encoding='ISO-8859-1')

similarity_df.set_index('track_name', inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Song Recommendation App"),
    dcc.Input(id='input-song', type='text', placeholder='Enter a song name...', debounce=True),
    html.Button('Get Recommendations', id='submit-val', n_clicks=0),
    html.Div(id='output-recommendations')
])

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

# Define callback to get song recommendations
@app.callback(
    Output('output-recommendations', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('input-song', 'value')]
)
def get_recommendations(n_clicks, input_song):
    if n_clicks > 0:
        recommendations = get_song_recommendations(input_song, num_recommendations=5)
        if isinstance(recommendations, list):
            return html.Ul([html.Li(song) for song in recommendations])
        else:
            return recommendations

if __name__ == '__main__':
    app.run_server(debug=True)
