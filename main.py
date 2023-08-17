import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
load_dotenv(".env")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=
                     SpotifyOAuth
                     (   
                         scope="playlist-modify-private",
                         redirect_uri="https://saransh-me.netlify.app",
                         client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         show_dialog=True,
                         cache_path="token.txt",
                         username="SaranshShank"
                     )
                    )
user_id = sp.current_user()["id"]
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
website_data = requests.get("https://www.billboard.com/charts/hot-100/" + date).text
soup = BeautifulSoup(website_data, "html.parser")
song_dict =  soup.find_all(name="h3", class_="a-no-trucate")
song_names = [song.getText().strip() for song in song_dict]
print(song_names)
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard Top 100", public=False)
playlist_id = playlist["id"]
print(playlist_id)
sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
#sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)