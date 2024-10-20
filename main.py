from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
class TimeMachine:

    def __init__(self):
        pass
    def get_songs_name(self, year):
        url = f"https://www.last.fm/tag/{year}/tracks"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the track listings
        tracks = []
        track_listings = soup.find_all('tr', class_='chartlist-row')

        for track in track_listings:
            # Extract the title and artist
            title = track.find('td', class_='chartlist-name').find('a').text.strip()
            artist = track.find('td', class_='chartlist-artist').find('a').text.strip()
            tracks.append({'title': title, 'artist': artist})

        return tracks
    def give_playlist(self,year):

        tracks = self.get_songs_name(year)
        song_name = []
        artists = []
        for i, track in enumerate(tracks, 1):
            song_name.append(track['title'])
            artists.append(track['artist'])

        sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    scope="playlist-modify-private",
                    redirect_uri="http://example.com",
                    client_id="9b4ce268e2024df6b9bb544ea77759f7",
                    client_secret="1961ab1123f24fc698026c206bf2938e",
                    show_dialog=True,
                    cache_path="token.txt",
                    username="Anuprash_02",
                )
            )
        user_id = sp.current_user()["id"]
        # Search Spotify for songs by title
        song_uris = []
        for song in song_name:
            result = sp.search(q=f"track:{song} year:{year}", type="track")

            # print(result["tracks"]["items"])
            if result["tracks"]["items"]==[]:
                continue
            else:
                uri = result["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
        playlist = sp.user_playlist_create(user=user_id, name=f"Best of year {year}", public=False)
        sp.playlist_add_items(playlist_id=playlist['id'],items=song_uris)
        link = playlist['external_urls']['spotify']
        return link

    def save_json(self, playlists, filename="playlists.json"):
        with open(filename, "w") as file:
            json.dump(playlists, file, indent=4)
        print(f"Playlists saved to {filename}")

    def load_json(self,filename="playlists.json"):
        try:
            with open(filename, "r") as file:
                playlists = json.load(file)
            return playlists
        except FileNotFoundError:
            return {}
# a = TimeMachine()
# link = a.give_playlist(1969)
# print(lin
# k)