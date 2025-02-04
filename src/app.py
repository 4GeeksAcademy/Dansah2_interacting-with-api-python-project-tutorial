import os
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import seaborn as sns
import matplotlib.pyplot as plt


# load the .env file variables
load_dotenv()

# obtain the client ID and Secret from the .env file
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# connect with the spotify API
spotify_connect = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret), requests_timeout=25)


# Get the top 10 of your favorite artist's songs. Keep the tracks element, which will contain the most played songs of the artist, 
# keep the name of the song, the popularity and the duration (in minutes).
sza_uri = '7tYKF4w9nC0nq9CsPZTHyP'
sza_data = spotify_connect.artist_top_tracks(sza_uri, country='US')
top_tracks = []

for i, track in enumerate(sza_data['tracks'][:10], 1):
    track_info = {
        'name': track['name'],
        'popularity': track['popularity'],
        'duration_min': round(track['duration_ms'] / 60000, 2)
    }
    top_tracks.append(track_info)

# Convert to a DataFrame.
top_tracks_df = pd.DataFrame(top_tracks)

# Sort the songs by increasing popularity and display the resulting top 3.
top_traks_df = top_tracks_df.sort_values(by='popularity', ascending=False)
print(top_tracks_df.head(3))


# Does duration have a relationship with popularity? 
# Are shorter songs more popular than longer songs? 
# Analyze it by plotting a scatter plot
sns.regplot(x=top_tracks_df['duration_min'], y=top_tracks_df['popularity'], scatter=True)
plt.title('Relationship between Song Duration and Popularity')
plt.xlabel('Duration in minutes')
plt.ylabel('Popularity')
plt.show()

# The scatterplot does not suggest a strong relationship between the duration of a song and its 
# popularity, therefore I could not say definitively that shorter songs are more popular than longer 
# songs. There is however a slight downward trend in popularity as the duration of a song increases.

